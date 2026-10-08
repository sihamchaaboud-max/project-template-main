"""
retrieve.py : contrat A -> B

    retrieve(query: str, k: int = 3) -> list[dict]
    chaque dict : {"id", "texte", "langue", "source_url", "theme"}
    (+ champs bonus : "categorie", "titre", "score")

"id" = id de la SOURCE (ex. "kvg_art64a" ou "kvg_art64a_de").

dedupe_langs=True (défaut) : si le même article remonte en FR et en DE,
on ne garde que la version la mieux classée. Le top-k contient donc
k articles DIFFÉRENTS.

Test rapide (depuis track_2b/) :
    python -m src.retrieve "Que se passe-t-il si je ne paie pas ma prime ?"
"""
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION = "jisr"
EMBED_MODEL = "BAAI/bge-m3"

_model = None
_col = None


def _load():
    global _model, _col
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    if _col is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _col = client.get_collection(COLLECTION)
    return _model, _col


def _article_key(source_id: str) -> str:
    """kvg_art64a_de -> kvg_art64a (même article, autre langue)."""
    return source_id[:-3] if source_id.endswith("_de") else source_id


def retrieve(
    query: str,
    k: int = 3,
    categorie: str | None = None,
    dedupe_langs: bool = True,
) -> list[dict]:
    model, col = _load()
    emb = model.encode([query], normalize_embeddings=True).tolist()
    where = {"categorie": categorie} if categorie else None
    # on demande beaucoup de chunks pour pouvoir filtrer les doublons
    n = min(max(k * 6, 15), col.count())
    res = col.query(query_embeddings=emb, n_results=n, where=where)

    out, seen = [], set()
    for meta, dist in zip(res["metadatas"][0], res["distances"][0]):
        key = _article_key(meta["source_id"]) if dedupe_langs else meta["source_id"]
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "id": meta["source_id"],
                "texte": meta["texte"],
                "langue": meta["langue"],
                "source_url": meta["source_url"],
                "theme": meta["theme"],
                "categorie": meta["categorie"],
                "titre": meta["titre"],
                "score": round(1 - dist, 4),
            }
        )
        if len(out) == k:
            break
    return out


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Je n'ai pas payé ma prime d'assurance maladie"
    for i, r in enumerate(retrieve(q), 1):
        print(f"\n[{i}] {r['id']}  ({r['langue']}, {r['theme']}, score {r['score']})")
        print(r["texte"][:200], "...")