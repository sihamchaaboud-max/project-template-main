"""
ingest.py : data/sources/<categorie>/*.txt  ->  chunks  ->  BGE-M3  ->  Chroma

Usage (depuis track_2b/) :
    python -m src.ingest

Format d'un fichier source :
    id: kvg_art64a
    titre: ...
    source: Fedlex
    url: https://...
    langue: fr
    theme: rappel
    date_acces: 2026-10-08
    ---
    (texte tel quel)

La catégorie = nom du dossier parent.
"""
import re
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "data" / "sources"
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION = "jisr"
EMBED_MODEL = "BAAI/bge-m3"
MAX_CHARS = 900  # taille max d'un chunk

# Lignes de notes de bas de page de Fedlex (début de ligne : numéro + formule).
# On ne touche PAS aux chiffres collés dans le texte (ex. "200712").
NOTE_RE = re.compile(
    r"^\d{1,3}\s+(Nouvelle teneur|Introdui|Abrog|Mise à jour|Voir |Corrig|RS \d|RO \d|FF \d|"
    r"Fassung|Eingefügt|Aufgehoben|Siehe|SR \d|AS \d|BBl|Berichtigt|Eingefuegt)",
    re.IGNORECASE,
)
# Ligne qui n'est qu'un marqueur de liste : "a." / "1." / "a.14" / "2.248"
MARKER_RE = re.compile(r"^[a-z0-9]{1,2}\.\d{0,3}$")
# Début d'alinéa : "1 ", "1bis ", "2 "...
ALINEA_RE = re.compile(r"^\d{1,2}(bis|ter|quater|quinquies|sexies|septies|octies)?\s")


def parse_file(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    if "---" not in raw:
        raise ValueError(f"{path.name} : ligne '---' manquante")
    head, body = raw.split("---", 1)
    meta = {}
    for line in head.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for champ in ("id", "titre", "url", "langue", "theme"):
        if champ not in meta:
            raise ValueError(f"{path.name} : champ '{champ}' manquant")
    return meta, body


def clean_body(body: str) -> list[str]:
    """Retire les notes, recolle les marqueurs, renvoie une liste de paragraphes."""
    lines = [l.strip() for l in body.splitlines()]
    lines = [l for l in lines if not NOTE_RE.match(l)]

    merged, i = [], 0
    while i < len(lines):
        l = lines[i]
        if MARKER_RE.match(l) and i + 1 < len(lines):
            # recolle "a." + texte suivant (on ignore le numéro de note collé)
            marker = l.split(".")[0] + "."
            nxt = lines[i + 1]
            merged.append(f"{marker} {nxt}")
            i += 2
        else:
            merged.append(l)
            i += 1

    # Regroupe en paragraphes : une ligne vide ou un début d'alinéa ouvre un paragraphe
    paras, cur = [], []
    for l in merged:
        if not l:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if ALINEA_RE.match(l) and cur:
            paras.append(" ".join(cur))
            cur = []
        cur.append(l)
    if cur:
        paras.append(" ".join(cur))
    return paras


def make_chunks(paras: list[str]) -> list[str]:
    """Assemble les paragraphes en chunks de MAX_CHARS caractères au plus."""
    chunks, cur = [], ""
    for p in paras:
        # paragraphe trop long : on le coupe par phrases
        pieces = [p]
        if len(p) > MAX_CHARS:
            pieces = re.split(r"(?<=[.;:])\s+", p)
        for piece in pieces:
            if cur and len(cur) + len(piece) + 1 > MAX_CHARS:
                chunks.append(cur)
                cur = piece
            else:
                cur = f"{cur} {piece}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def main() -> None:
    files = sorted(SOURCES_DIR.glob("*/*.txt"))
    if not files:
        sys.exit(f"Aucun fichier trouvé dans {SOURCES_DIR}")

    ids, docs, metas = [], [], []
    seen_ids = set()
    for path in files:
        meta, body = parse_file(path)
        if meta["id"] in seen_ids:
            sys.exit(f"id en double : {meta['id']}")
        seen_ids.add(meta["id"])
        if meta["id"] != path.stem:
            print(f"ATTENTION : id '{meta['id']}' différent du nom de fichier '{path.name}'")

        categorie = path.parent.name
        chunks = make_chunks(clean_body(body))
        for n, ch in enumerate(chunks):
            ids.append(f"{meta['id']}#{n}")
            # le titre est ajouté au texte indexé pour aider la recherche
            docs.append(f"{meta['titre']}\n{ch}")
            metas.append(
                {
                    "source_id": meta["id"],
                    "titre": meta["titre"],
                    "source_url": meta["url"],
                    "langue": meta["langue"],
                    "theme": meta["theme"],
                    "categorie": categorie,
                    "chunk": n,
                    "texte": ch,
                }
            )
        print(f"{categorie}/{path.name} : {len(chunks)} chunk(s)")

    print(f"\nTotal : {len(files)} fichiers, {len(docs)} chunks. Chargement de {EMBED_MODEL}...")
    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(docs, normalize_embeddings=True, show_progress_bar=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        client.delete_collection(COLLECTION)  # on reconstruit à zéro
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    col.add(ids=ids, documents=docs, embeddings=embeddings.tolist(), metadatas=metas)
    print(f"OK : {col.count()} chunks indexés dans {CHROMA_DIR}")


if __name__ == "__main__":
    main()