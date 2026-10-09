"""
eval/run_eval.py : benchmark principal de Jisr (extraction + chiffres + citation)

Pour chaque courrier de data/testset.json :
  1. Extraction (Apertus) -> JSON : categorie, type_document, delai, montant, action_demandee
  2. Recherche (RAG)      -> top-3 articles, requête = courrier complet
  3. Notes :
       json_ok     : le modèle a renvoyé un JSON exploitable
       categorie   : catégorie extraite == catégorie attendue
       delai       : date exacte (AAAA-MM-JJ)
       montant     : nombre exact (null attendu -> null obtenu)
       citation    : - courrier avec source : une source attendue est dans le top-3
                     - courrier "autre"     : Jisr ne cite rien
                       (categorie extraite "autre" OU meilleur score < SEUIL)

Non noté automatiquement : type_document (étiquette libre), action_demandee
(à relire à la main), qualité de la darija (locuteur natif).

Usage (depuis track_2b/) :
    python -m eval.run_eval --fake                 # test du script, SANS modèle
    python -m eval.run_eval --model 8b
    python -m eval.run_eval --model 70b
    python -m eval.run_eval --model 8b --limit 5   # 5 premiers courriers
"""
import argparse
import json
import re
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"
SEUIL_SOURCE = 0.54  # sous ce score du meilleur passage : "pas de source officielle"

# ---------------------------------------------------------------------------
# Prompt d'extraction PROVISOIRE : à remplacer par celui de src/prompts.py (B)
# ---------------------------------------------------------------------------
EXTRACTION_PROMPT = """Tu lis un courrier officiel suisse (allemand ou français).
Réponds UNIQUEMENT avec un objet JSON, sans texte autour, avec ces clés :
- "categorie" : une valeur parmi "assurance_maladie", "rappel_poursuite", "sejour", "autre"
- "type_document" : court, en minuscules avec underscores (ex. "commandement_de_payer")
- "delai" : la date limite la plus proche que la personne doit respecter, au format AAAA-MM-JJ.
  Si le délai est relatif (« dans les dix jours »), calcule-le à partir de la date de notification
  ou de la date du courrier. null s'il n'y a aucun délai.
- "montant" : le montant total à payer en CHF s'il est écrit, sinon le montant principal,
  comme nombre (ex. 1250.00). null s'il n'y a aucun montant.
- "action_demandee" : ce que la personne doit faire, en une phrase.

Date du courrier : {date_courrier}

Courrier :
\"\"\"
{courrier}
\"\"\"
"""


def fake_extract(t: dict, i: int) -> str:
    """Faux modèle : renvoie l'attendu avec des erreurs volontaires (test du script)."""
    att = t["attendu"]
    out = {
        "categorie": t["categorie"],
        "type_document": att["type_document"],
        "delai": att["delai"],
        "montant": att["montant"],
        "action_demandee": att["action_demandee"],
    }
    if i == 6:
        return "Désolé, je ne peux pas répondre en JSON."  # JSON invalide
    if i % 4 == 3 and out["montant"] is not None:
        out["montant"] = out["montant"] + 20  # mauvais montant
    if i % 5 == 4:
        out["delai"] = "2026-10-01"  # mauvaise date
    if i % 7 == 5:
        out["categorie"] = "autre"  # mauvaise catégorie
    return "```json\n" + json.dumps(out, ensure_ascii=False) + "\n```"


def parse_json(text: str):
    """Extrait un objet JSON d'une réponse de LLM (gère les ```json et le texte autour)."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    a, b = text.find("{"), text.rfind("}")
    if a == -1 or b <= a:
        return None
    try:
        obj = json.loads(text[a : b + 1])
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def to_number(x):
    if x is None:
        return None
    try:
        return float(str(x).replace("'", "").replace("’", "").replace(",", ".").strip())
    except ValueError:
        return "invalide"


def norm(source_id: str) -> str:
    return source_id[:-3] if source_id.endswith("_de") else source_id


def main(model: str, fake: bool, limit: int | None) -> None:
    tests = json.loads(TESTSET.read_text(encoding="utf-8"))
    if limit:
        tests = tests[:limit]

    if not fake:
        from src.llm import call_llm
    from src.retrieve import retrieve

    tag = ("fake" if fake else model)
    rows, raws = [], []
    for i, t in enumerate(tests):
        att = t["attendu"]

        # --- 1. extraction
        t0 = time.time()
        if fake:
            raw = fake_extract(t, i)
        else:
            prompt = EXTRACTION_PROMPT.format(
                date_courrier=t["date_courrier"], courrier=t["courrier"]
            )
            raw = call_llm(prompt, model=model, temperature=0)
        latence = time.time() - t0
        got = parse_json(raw)

        # --- 2. recherche (requête = courrier complet)
        res = retrieve(t["courrier"], k=3)
        top_ids = [norm(r["id"]) for r in res]
        top_score = res[0]["score"] if res else 0.0

        # --- 3. notes
        row = {"id": t["id"], "categorie": t["categorie"], "langue": t["langue"],
               "latence_s": round(latence, 2), "json_ok": int(got is not None)}
        if got is not None:
            row["cat_ok"] = int(got.get("categorie") == t["categorie"])
            row["delai_ok"] = int(str(got.get("delai")) == str(att["delai"])
                                  or (att["delai"] is None and got.get("delai") is None))
            g_m, a_m = to_number(got.get("montant")), att["montant"]
            if a_m is None:
                row["montant_ok"] = int(g_m is None)
            else:
                row["montant_ok"] = int(isinstance(g_m, float) and abs(g_m - float(a_m)) < 0.005)
            predit_autre = got.get("categorie") == "autre"
        else:
            row.update(cat_ok=0, delai_ok=0, montant_ok=0)
            predit_autre = False  # sans JSON on ne sait pas : on se fie au score

        ne_cite_rien = predit_autre or top_score < SEUIL_SOURCE
        expected = [norm(s) for s in t["source_ids_attendus"]]
        if t["categorie"] == "autre":
            row["citation_ok"] = int(ne_cite_rien)
        else:
            row["citation_ok"] = int(any(s in top_ids for s in expected) and not ne_cite_rien)
        row["montant_attendu"] = att["montant"]
        rows.append(row)
        raws.append({"id": t["id"], "sortie_brute": raw, "json": got,
                     "attendu": att, "top3": top_ids, "top_score": top_score})

    # --- agrégation
    def pct(rs, key):
        return f"{sum(r[key] for r in rs) / len(rs):.0%}" if rs else "n/a"

    titre = "FAKE (test du script, ces chiffres ne sont PAS des résultats)" if fake else f"Apertus {model}"
    L = [f"# Benchmark extraction + citation : {titre}\n",
         f"Courriers : {len(rows)}. Seuil de source : {SEUIL_SOURCE}.\n",
         "## Global\n",
         f"- JSON exploitable : **{pct(rows, 'json_ok')}**",
         f"- Catégorie : **{pct(rows, 'cat_ok')}**",
         f"- Délai exact : **{pct(rows, 'delai_ok')}**",
         f"- Montant exact : **{pct(rows, 'montant_ok')}**",
         f"- Citation correcte : **{pct(rows, 'citation_ok')}**",
         f"- Latence moyenne d'extraction : {sum(r['latence_s'] for r in rows) / len(rows):.2f} s\n"]

    for champ, nom in (("categorie", "Par catégorie"), ("langue", "Par langue")):
        g = defaultdict(list)
        for r in rows:
            g[r[champ]].append(r)
        L += [f"## {nom}\n",
              f"| {champ} | n | JSON | catégorie | délai | montant | citation |",
              "|---|---|---|---|---|---|---|"]
        for k, rs in sorted(g.items()):
            L.append(f"| {k} | {len(rs)} | {pct(rs, 'json_ok')} | {pct(rs, 'cat_ok')} | "
                     f"{pct(rs, 'delai_ok')} | {pct(rs, 'montant_ok')} | {pct(rs, 'citation_ok')} |")
        L.append("")

    avec = [r for r in rows if r["montant_attendu"] is not None]
    sans = [r for r in rows if r["montant_attendu"] is None]
    L += ["## Montant : avec et sans montant dans le courrier\n",
          f"- Courriers avec montant ({len(avec)}) : {pct(avec, 'montant_ok')}",
          f"- Courriers sans montant, `null` attendu ({len(sans)}) : {pct(sans, 'montant_ok')}\n",
          "## Détail\n",
          "| id | catégorie | JSON | catég. | délai | montant | citation |",
          "|---|---|---|---|---|---|---|"]
    ok = lambda v: "OK" if v else "RATE"
    for r in rows:
        L.append(f"| {r['id']} | {r['categorie']} | {ok(r['json_ok'])} | {ok(r['cat_ok'])} | "
                 f"{ok(r['delai_ok'])} | {ok(r['montant_ok'])} | {ok(r['citation_ok'])} |")

    out_md = ROOT / "eval" / f"results_extraction_{tag}.md"
    out_json = ROOT / "eval" / f"raw_extraction_{tag}.json"
    out_md.write_text("\n".join(L), encoding="utf-8")
    out_json.write_text(json.dumps(raws, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(L))
    print(f"\n(écrit dans {out_md} et {out_json})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="8b", choices=["8b", "70b"])
    ap.add_argument("--fake", action="store_true", help="faux modèle, pour tester le script")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    main(a.model, a.fake, a.limit)