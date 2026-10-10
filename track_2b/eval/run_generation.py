"""
eval/run_generation.py : évaluation de la génération en darija (glossaire / exemples)

Pour chaque courrier du jeu de test :
  1. extraction (pipeline de B) et recherche des passages : UNE fois, partagées par les variantes
  2. règle recommandée : meilleur score < 0.54  ->  aucun passage ("pas de source officielle")
  3. génération de l'explication, une fois par variante :
       full         : glossaire + exemples (comportement actuel de B)
       no_glossary  : exemples, sans glossaire
       baseline     : ni glossaire, ni exemples
  4. contrôles automatiques + feuille de notation ANONYMISÉE pour le locuteur natif

Contrôles automatiques (aucun ne mesure la qualité de la darija) :
  check_ok       : check.py de B (les nombres extraits figurent dans la réponse)
  montant_ok     : le montant attendu figure dans la réponse (si un montant est attendu)
  date_ok        : le jour ET l'année de la date attendue figurent dans la réponse
                   (échoue aussi quand l'EXTRACTION s'est trompée d'échéance)
  non_soutenus   : réponses contenant un nombre > 31 absent du courrier, des passages et de
                   l'attendu (les nombres des URL sont ignorés ; indice à relire à la main)
  arabe          : part des lettres en écriture arabe (une réponse en français = faible)
  source_citee   : l'id ou l'URL d'un passage, "fedlex", un article (art. 64a, المادة 64)
                   ou une loi (LAMal, KVG, LP, SchKG, LEI, AIG) figure dans la réponse

La qualité de la darija ne se mesure QUE par une personne qui parle darija :
voir eval/rating_sheet_<modèle>.csv (variantes anonymisées).
Pour LIRE les réponses avec leurs variantes : eval/answers_<modèle>.md.

Usage (depuis track_2b/) :
    python -m eval.run_generation --model 8b --limit 3
    python -m eval.run_generation --model 8b
    python -m eval.run_generation --model 70b
"""
import argparse
import csv
import json
import random
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"
SEUIL_SOURCE = 0.54
ARABIC = re.compile(r"[\u0600-\u06FF]")
URL_RE = re.compile(r"(?:https?://|www\.)\S+|\S*fedlex\.admin\.ch\S*", re.I)
LAW_RE = re.compile(
    r"(?<![A-Za-z])(?:art\.?|article|artikel)\s*\d+"
    r"|المادة\s*\d+"
    r"|(?<![A-Za-z])(?:LAMal|KVG|SchKG|LEI|AIG|LP)(?![A-Za-z])",
    re.I,
)
CONDITIONS = ["full", "no_glossary", "baseline"]


def canon(n: str) -> str:
    s = n.replace("'", "").replace("’", "")
    if re.fullmatch(r"\d+,\d{1,2}", s):
        s = s.replace(",", ".")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if re.fullmatch(r"\d+", s):
        s = str(int(s))
    return s


def nums(text: str) -> set:
    from src.check import normaliser
    text = URL_RE.sub(" ", text or "")
    return {canon(n) for n in re.findall(r"\d+(?:[.,'’]\d+)*", normaliser(text))}


def unsupported(answer: str, support: set) -> list:
    out = []
    for n in nums(answer):
        if n in support:
            continue
        if re.fullmatch(r"\d+", n) and int(n) <= 31:
            continue
        out.append(n)
    return sorted(out)


def arabic_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    return sum(1 for c in letters if ARABIC.match(c)) / len(letters) if letters else 0.0


def source_cited(answer: str, passages: list):
    if not passages:
        return None
    if any(p.get("id", "@@") in answer or (p.get("source_url") and p["source_url"] in answer)
           for p in passages):
        return 1
    return int("fedlex" in answer.lower() or bool(LAW_RE.search(answer)))


def main(model, limit, temperature, apply_threshold):
    import src.prompts as P
    from src.check import check_answer
    from src.llm import call_llm
    from src.pipeline import extract, get_passages

    tests = json.loads(TESTSET.read_text(encoding="utf-8"))
    if limit:
        tests = tests[:limit]

    glossary = P.load_glossary()
    filled = [e for e in glossary if e.get("darija")]
    print(f"Glossaire : {len(glossary)} entrées, dont {len(filled)} avec une traduction darija.")
    if not filled:
        print("ATTENTION : aucune traduction darija dans le glossaire : 'full' = 'no_glossary'.")
    orig_examples = P.load_examples

    def set_examples(on: bool):
        P.load_examples = orig_examples if on else (lambda path=None: "(aucun exemple)")

    results, rng = [], random.Random(42)
    for t in tests:
        print(f"{t['id']} ...", flush=True)
        att = t["attendu"]
        extraction, ok = extract(t["courrier"], model)
        passages, warn = get_passages(t["courrier"], extraction)
        top_score = passages[0].get("score", 0.0) if passages else 0.0
        abstain = apply_threshold and top_score < SEUIL_SOURCE
        if abstain:
            passages = []

        support = nums(t["courrier"])
        if att["montant"] is not None:
            support |= {canon(f"{att['montant']:.2f}")}
        for p in passages:
            support |= nums(p.get("texte", ""))
        if att["delai"]:
            support |= {canon(att["delai"][:4]), canon(att["delai"][8:10])}

        entry = {"id": t["id"], "categorie": t["categorie"], "langue": t["langue"],
                 "extraction": extraction, "extraction_ok": ok, "top_score": top_score,
                 "sans_source": int(abstain), "passages": [p["id"] for p in passages],
                 "variantes": {}}
        for cond in CONDITIONS:
            set_examples(cond in ("full", "no_glossary"))
            gl = glossary if cond == "full" else []
            t0, erreur, reponse = time.time(), None, ""
            try:
                prompt = P.build_explanation_prompt(t["courrier"], extraction, passages, glossaire=gl)
                reponse = call_llm(prompt, model=model, system=P.SYSTEM_PROMPT,
                                   temperature=temperature, max_tokens=900)
            except Exception as e:  # noqa: BLE001
                erreur = f"{type(e).__name__}: {e}"
            latence = round(time.time() - t0, 2)
            m_ok = None
            if att["montant"] is not None:
                m_ok = int(canon(f"{att['montant']:.2f}") in nums(reponse))
            d_ok = None
            if att["delai"]:
                n_rep = nums(reponse)
                d_ok = int(canon(att["delai"][:4]) in n_rep and canon(att["delai"][8:10]) in n_rep)
            chk = check_answer(extraction, reponse) if reponse else {"ok": False, "manquants": ["(vide)"]}
            entry["variantes"][cond] = {
                "reponse": reponse, "erreur": erreur, "latence_s": latence,
                "check_ok": int(chk["ok"]), "manquants": chk["manquants"],
                "montant_ok": m_ok, "date_ok": d_ok,
                "non_soutenus": unsupported(reponse, support),
                "arabe": round(arabic_ratio(reponse), 2),
                "source_citee": source_cited(reponse, passages),
                "longueur": len(reponse)}
        results.append(entry)
    set_examples(True)

    # ---- agrégation
    def mean(vals):
        vals = [v for v in vals if v is not None]
        return f"{sum(vals) / len(vals):.0%}" if vals else "n/a"

    sans = [r["id"] for r in results if r["sans_source"]]
    L = [f"# Génération en darija : Apertus {model}, température {temperature}\n",
         f"Courriers : {len(results)}. Glossaire : {len(filled)} traductions darija. "
         f"Règle « sans source » (score < {SEUIL_SOURCE}) : "
         f"{'appliquée' if apply_threshold else 'désactivée'}.",
         f"Courriers sans passage ({len(sans)}) : {', '.join(sans) or 'aucun'}\n",
         "Ces contrôles sont automatiques : AUCUN ne mesure la qualité de la darija "
         "(voir la feuille de notation).\n",
         "| Variante | n | check.py de B | montant dans la réponse | date dans la réponse | "
         "nombres non soutenus | écriture arabe | source citée | longueur moy. | latence moy. |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for cond in CONDITIONS:
        v = [r["variantes"][cond] for r in results]
        nonsup = sum(1 for x in v if x["non_soutenus"])
        L.append(f"| {cond} | {len(v)} | {mean([x['check_ok'] for x in v])} | "
                 f"{mean([x['montant_ok'] for x in v])} | {mean([x['date_ok'] for x in v])} | "
                 f"{nonsup}/{len(v)} | {sum(x['arabe'] for x in v) / len(v):.0%} | "
                 f"{mean([x['source_citee'] for x in v])} | "
                 f"{sum(x['longueur'] for x in v) // len(v)} | "
                 f"{sum(x['latence_s'] for x in v) / len(v):.1f} s |")
    L += ["", "## Réponses qui échouent à check.py (nombres extraits absents de la réponse)\n"]
    for r in results:
        for cond in CONDITIONS:
            mq = r["variantes"][cond]["manquants"]
            if mq:
                L.append(f"- {r['id']} / {cond} : {'; '.join(mq)}")
    L += ["", "## Réponses avec des nombres non soutenus (à relire)\n"]
    for r in results:
        for cond in CONDITIONS:
            ns = r["variantes"][cond]["non_soutenus"]
            if ns:
                L.append(f"- {r['id']} / {cond} : {', '.join(ns)}")
    erreurs = [(r["id"], c) for r in results for c in CONDITIONS if r["variantes"][c]["erreur"]]
    L.append(f"\nErreurs d'appel : {len(erreurs)}")

    ev = ROOT / "eval"
    (ev / f"results_generation_{model}.md").write_text("\n".join(L), encoding="utf-8")
    (ev / f"generation_{model}.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- fichier de lecture (NON anonymisé : pour l'équipe, pas pour la locutrice)
    A = [f"# Réponses générées : Apertus {model} (lecture par l'équipe, variantes visibles)\n"]
    for r in results:
        A.append(f"\n## {r['id']} ({r['categorie']}, {r['langue']})\n")
        A.append(f"Extraction : `{json.dumps(r['extraction'], ensure_ascii=False)}`  ")
        A.append(f"Passages : {', '.join(r['passages']) or 'aucun (règle sans source)'} "
                 f"(meilleur score {r['top_score']})\n")
        for cond in CONDITIONS:
            v = r["variantes"][cond]
            A.append(f"### {cond}\n\n{v['reponse']}\n")
            A.append(f"_check.py: {'OK' if v['check_ok'] else 'ECHEC ' + str(v['manquants'])} | "
                     f"arabe {v['arabe']:.0%} | source citée: {v['source_citee']} | "
                     f"non soutenus: {v['non_soutenus'] or '-'}_\n")
    (ev / f"answers_{model}.md").write_text("\n".join(A), encoding="utf-8")

    # ---- feuille de notation anonymisée
    key, rows = {}, []
    for r in results:
        conds = CONDITIONS[:]
        rng.shuffle(conds)
        key[r["id"]] = {}
        for label, cond in zip("ABC", conds):
            key[r["id"]][label] = cond
            rows.append([r["id"], label, r["variantes"][cond]["reponse"], "", "", "", "", ""])
    with open(ev / f"rating_sheet_{model}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id_courrier", "variante", "reponse", "darija_reelle_1a5", "sens_correct_1a5",
                    "chiffres_intacts_1a5", "clarte_1a5", "commentaire"])
        w.writerows(rows)
    (ev / f"rating_key_{model}.json").write_text(json.dumps(key, indent=2), encoding="utf-8")

    print("\n".join(L))
    print(f"\n(écrit dans eval/results_generation_{model}.md, generation_{model}.json, "
          f"answers_{model}.md, rating_sheet_{model}.csv et rating_key_{model}.json)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="8b", choices=["8b", "70b"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--no-threshold", action="store_true")
    a = ap.parse_args()
    main(a.model, a.limit, a.temperature, not a.no_threshold)