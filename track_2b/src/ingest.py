"""
ingest.py : data/sources/<categorie>/*.txt  ->  chunks  ->  BGE-M3  ->  Chroma

Usage (depuis track_2b/) :
    python -m src.ingest          # reconstruit TOUJOURS l'index

Dans le code :
    from src.ingest import ensure_index
    ensure_index()                # construit l'index seulement s'il n'existe pas (app.py)

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

Corrections de cette version :
  - ensure_index() : appelée par app.py au démarrage ; sans elle, l'application ne construisait
    pas la base (« ingest.py absent : démarrage sans index »)
  - le numéro de note de bas de page collé au titre de l'article est retiré
    ("Art. 65264" -> "Art. 65", "Art. 64a251" -> "Art. 64a"), en s'appuyant sur le numéro
    d'article de l'id du fichier ; seul le TITRE de l'article est touché
  - le titre de la loi ("Loi fédérale sur l'assurance-maladie, art. 64a") est placé devant
    chaque passage renvoyé par retrieve()
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


def clean_body(body: str, art_num: str | None = None) -> list[str]:
    """Retire les notes, nettoie le titre de l'article, recolle les marqueurs, renvoie des paragraphes."""
    lines = [l.strip() for l in body.splitlines()]
    lines = [l for l in lines if not NOTE_RE.match(l)]

    # "Art. 65264 Prämienverbilligung" -> "Art. 65 Prämienverbilligung" (premier titre seulement)
    if art_num:
        heading = re.compile(rf"^(Art\.\s*{re.escape(art_num)})\d{{1,3}}(?=\s|$)")
        for i, l in enumerate(lines):
            if heading.match(l):
                lines[i] = heading.sub(r"\1", l)
                break

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


def build_index() -> int:
    """Lit les sources, calcule les embeddings et (re)crée la collection. Renvoie le nb de chunks.

    Lève FileNotFoundError ou ValueError (jamais sys.exit) pour ne pas faire planter l'application.
    """
    files = sorted(SOURCES_DIR.glob("*/*.txt"))
    if not files:
        raise FileNotFoundError(f"Aucun fichier source trouvé dans {SOURCES_DIR}")

    ids, docs, metas = [], [], []
    seen_ids = set()
    for path in files:
        meta, body = parse_file(path)
        if meta["id"] in seen_ids:
            raise ValueError(f"id en double : {meta['id']}")
        seen_ids.add(meta["id"])
        if meta["id"] != path.stem:
            print(f"ATTENTION : id '{meta['id']}' différent du nom de fichier '{path.name}'")

        m = re.search(r"_art(\d+[a-z]?)(?:_de)?$", meta["id"])
        art_num = m.group(1) if m else None

        categorie = path.parent.name
        chunks = make_chunks(clean_body(body, art_num))
        for n, ch in enumerate(chunks):
            ids.append(f"{meta['id']}#{n}")
            # le titre est ajouté au texte indexé ET au texte renvoyé par retrieve()
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
                    "texte": f"{meta['titre']}\n{ch}",
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
    return col.count()


def ensure_index(force: bool = False) -> None:
    """Construit l'index seulement s'il n'existe pas (ou est vide). Appelée par app.py au démarrage.

    Après un `git clone`, data/chroma/ n'existe pas : la première exécution construit la base
    (1 à 2 minutes sur CPU, BGE-M3 doit être disponible). Les suivantes démarrent tout de suite.
    Pour reconstruire après avoir modifié les sources : `python -m src.ingest`.
    """
    if not force:
        try:
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            if client.get_collection(COLLECTION).count() > 0:
                return
        except Exception:
            pass
        print("Index absent : construction au premier démarrage...")
    build_index()


def main() -> None:
    try:
        build_index()
    except (FileNotFoundError, ValueError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()