"""
eval/eval_retrieval.py : score de la recherche (RAG seul, sans LLM)

Modes de requête (--query) :
  courrier : le texte complet du courrier (défaut)
  oracle   : type_document + action_demandee ATTENDUS du jeu de test,
             comme si l'extraction d'Apertus était parfaite
             (borne haute du gain ; le vrai chiffre viendra avec l'extraction réelle)

Métriques : hit@k, rappel@k, MRR (suffixe _de retiré avant comparaison).
Courriers sans source attendue (categorie "autre") : exclus des scores,
on affiche le meilleur score de recherche.

Usage (depuis track_2b/) :
    python -m eval.eval_retrieval
    python -m eval.eval_retrieval --query oracle
    python -m eval.eval_retrieval --no-dedupe
    python -m eval.eval_retrieval --k 5
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from src.retrieve import retrieve

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"


def norm(source_id: str) -> str:
    return source_id[:-3] if source_id.endswith("_de") else source_id


def build_query(t: dict, mode: str) -> str:
    if mode == "oracle":
        att = t["attendu"]
        type_doc = att["type_document"].replace("_", " ")
        return f"{type_doc}. {att['action_demandee']}"
    return t["courrier"]


def main(k: int, dedupe: bool, mode: str) -> None:
    tests = json.loads(TESTSET.read_text(encoding="utf-8"))
    desc = f"requête={mode}, " + ("avec" if dedupe else "sans") + " dédoublonnage FR/DE"
    suffix = f"_{mode}" + ("" if dedupe else "_nodedupe")
    out_path = ROOT / "eval" / f"results_retrieval{suffix}.md"

    rows = []
    for t in tests:
        res = retrieve(build_query(t, mode), k=k, dedupe_langs=dedupe)
        got = [norm(r["id"]) for r in res]
        expected = [norm(s) for s in t["source_ids_attendus"]]
        row = {
            "id": t["id"],
            "categorie": t["categorie"],
            "langue": t["langue"],
            "attendu": expected,
            "obtenu": got,
            "top_score": res[0]["score"] if res else 0.0,
        }
        if expected:
            found = [s for s in expected if s in got]
            row["hit"] = 1 if found else 0
            row["rappel"] = len(found) / len(expected)
            ranks = [got.index(s) + 1 for s in expected if s in got]
            row["mrr"] = 1 / min(ranks) if ranks else 0.0
        rows.append(row)

    scored = [r for r in rows if "hit" in r]

    def avg(rs, key):
        return sum(r[key] for r in rs) / len(rs) if rs else float("nan")

    L = [f"# Score de recherche (top-{k}, {desc})\n"]
    L.append(f"Courriers évalués : {len(scored)} (sur {len(rows)})\n")
    L.append("## Global\n")
    L.append(f"- hit@{k} : **{avg(scored, 'hit'):.0%}**")
    L.append(f"- rappel@{k} : **{avg(scored, 'rappel'):.0%}**")
    L.append(f"- MRR : **{avg(scored, 'mrr'):.2f}**\n")

    for champ, titre in (("categorie", "Par catégorie"), ("langue", "Par langue")):
        groups = defaultdict(list)
        for r in scored:
            groups[r[champ]].append(r)
        L.append(f"## {titre}\n")
        L.append(f"| {champ} | n | hit@{k} | rappel@{k} | MRR |")
        L.append("|---|---|---|---|---|")
        for g, rs in sorted(groups.items()):
            L.append(
                f"| {g} | {len(rs)} | {avg(rs, 'hit'):.0%} | "
                f"{avg(rs, 'rappel'):.0%} | {avg(rs, 'mrr'):.2f} |"
            )
        L.append("")

    L.append("## Détail\n")
    L.append("| id | catégorie | attendu | obtenu | hit |")
    L.append("|---|---|---|---|---|")
    for r in rows:
        hit = "-" if "hit" not in r else ("OK" if r["hit"] else "RATE")
        L.append(
            f"| {r['id']} | {r['categorie']} | {', '.join(r['attendu']) or '(aucune)'} "
            f"| {', '.join(r['obtenu'])} | {hit} |"
        )
    L.append("")

    sans = [r for r in rows if "hit" not in r]
    if sans:
        L.append("## Courriers sans source attendue (seuil possible)\n")
        for r in sans:
            L.append(
                f"- {r['id']} ({r['categorie']}) : meilleur passage = "
                f"{r['obtenu'][0]}, score {r['top_score']}"
            )
        scores = [r["top_score"] for r in scored]
        L.append(
            f"\nCourriers avec source : score du meilleur passage, "
            f"min {min(scores):.3f}, moyenne {avg(scored, 'top_score'):.3f}, "
            f"max {max(scores):.3f}"
        )
        L.append(
            "Un seuil n'est fiable que si le MIN des courriers avec source "
            "reste au-dessus du MAX des courriers hors périmètre."
        )

    texte = "\n".join(L)
    out_path.write_text(texte, encoding="utf-8")
    print(texte)
    print(f"\n(écrit dans {out_path})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--no-dedupe", action="store_true")
    ap.add_argument("--query", choices=["courrier", "oracle"], default="courrier")
    a = ap.parse_args()
    main(a.k, dedupe=not a.no_dedupe, mode=a.query)