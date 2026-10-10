"""
eval/score_sources.py : la source citée dans la réponse est-elle la bonne ?

Lit eval/generation_<modèle>.json (produit par run_generation.py) : AUCUN appel au modèle.
Extrait les numéros d'articles cités dans chaque réponse (art. 64a, Art. 69, المادة 69 و74...)
et les compare aux numéros des source_ids_attendus du jeu de test.

Pour chaque variante, sur les courriers qui avaient des passages ET une source attendue :
  correct       : au moins un article cité fait partie des sources attendues
  faux          : un article est cité, mais aucun n'est attendu (loi plausible mais fausse)
  aucun_article : aucun article cité (la réponse renvoie à la lettre seulement)
Sur les courriers sans passage (règle "sans source") ou sans source attendue :
  cite_un_article : doit valoir 0 (sinon, autorité juridique inventée)

Limite : on compare des NUMÉROS d'articles. Citer le bon numéro dans la mauvaise loi
passerait ; citer un article défendable mais non prévu par le jeu de test compte "faux".

Usage (depuis track_2b/) :
    python -m eval.score_sources --model 8b
    python -m eval.score_sources --model 70b
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"
CONDITIONS = ["full", "no_glossary", "baseline"]

ART = re.compile(
    r"(?<![A-Za-z])(?:art\.?|article|artikel|المادة)\s*"
    r"(\d+[a-z]?(?:\s*(?:و|,|et|und|/|&)\s*(?:المادة|art\.?|article|artikel)?\s*\d+[a-z]?)*)",
    re.I,
)
NUM = re.compile(r"\d+[a-z]?", re.I)


def cited_numbers(text: str) -> set:
    from src.check import normaliser
    out = set()
    for m in ART.finditer(normaliser(text or "")):
        out |= {n.lower() for n in NUM.findall(m.group(1))}
    return out


def expected_numbers(ids: list) -> set:
    out = set()
    for i in ids:
        i = i[:-3] if i.endswith("_de") else i
        m = re.search(r"_art(\d+[a-z]?)$", i)
        if m:
            out.add(m.group(1).lower())
    return out


def main(model: str) -> None:
    results = json.loads((ROOT / "eval" / f"generation_{model}.json").read_text(encoding="utf-8"))
    tests = {t["id"]: t for t in json.loads(TESTSET.read_text(encoding="utf-8"))}

    stats = {c: {"correct": 0, "faux": 0, "aucun_article": 0, "sans_source_cite": 0,
                 "sans_source_n": 0} for c in CONDITIONS}
    faux, sans_cite = [], []
    for r in results:
        exp = expected_numbers(tests[r["id"]]["source_ids_attendus"])
        for cond in CONDITIONS:
            cited = cited_numbers(r["variantes"][cond]["reponse"])
            s = stats[cond]
            if r["sans_source"] or not exp:
                s["sans_source_n"] += 1
                if cited:
                    s["sans_source_cite"] += 1
                    sans_cite.append(f"- {r['id']} / {cond} : cite {sorted(cited)} sans source attendue")
            elif not cited:
                s["aucun_article"] += 1
            elif cited & exp:
                s["correct"] += 1
            else:
                s["faux"] += 1
                faux.append(f"- {r['id']} / {cond} : cite {sorted(cited)}, attendu {sorted(exp)}")

    L = [f"# Sources citées : Apertus {model}\n",
         "Courriers avec passages ET source attendue :\n",
         "| Variante | n | article correct | article faux | aucun article cité |",
         "|---|---|---|---|---|"]
    for cond in CONDITIONS:
        s = stats[cond]
        n = s["correct"] + s["faux"] + s["aucun_article"]
        pc = lambda k: f"{s[k]}/{n} ({s[k] / n:.0%})" if n else "n/a"
        L.append(f"| {cond} | {n} | {pc('correct')} | {pc('faux')} | {pc('aucun_article')} |")
    L += ["", "Courriers sans passage ou sans source attendue (aucun article ne doit être cité) :\n",
          "| Variante | n | réponses qui citent un article |", "|---|---|---|"]
    for cond in CONDITIONS:
        s = stats[cond]
        L.append(f"| {cond} | {s['sans_source_n']} | {s['sans_source_cite']} |")
    L += ["", "## Citations fausses (à relire)\n"] + (faux or ["(aucune)"])
    L += ["", "## Articles cités sans source attendue (à relire)\n"] + (sans_cite or ["(aucun)"])

    out = ROOT / "eval" / f"results_sources_{model}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n(écrit dans {out})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="8b", choices=["8b", "70b"])
    main(ap.parse_args().model)