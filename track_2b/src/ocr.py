"""
ocr.py : lit le texte d'une photo de courrier, EN LOCAL (Tesseract, français + allemand).

L'image ne quitte pas l'ordinateur : seul le texte lu est envoyé ensuite au pipeline.
Le texte doit TOUJOURS être relu par la personne avant l'explication (une erreur de chiffre
ne serait détectée par aucun contrôle en aval).

Prérequis :
  - Tesseract installé, avec les données de langue "fra" et "deu"
      Windows : installateur UB Mannheim (cocher French et German), ou
                winget install --id UB-Mannheim.TesseractOCR  puis ajouter fra.traineddata et
                deu.traineddata dans un dossier, et définir TESSDATA_PREFIX vers ce dossier
      Docker  : apt-get install tesseract-ocr tesseract-ocr-fra tesseract-ocr-deu
  - pip install pytesseract pillow
  - variable TESSERACT_CMD (facultative) si tesseract n'est pas dans le PATH

Utilisation :
    from src.ocr import read_photo, read_upload
    texte, message = read_photo(image)        # image PIL ou tableau numpy
    texte, message = read_upload(chemin)      # fichier téléversé (Gradio)

Test en ligne de commande (depuis track_2b/) :
    python -m src.ocr chemin\\vers\\photo.jpg
"""
import os
import shutil
import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image, ImageOps
except ImportError:  # dépendances absentes : la lecture de photo est désactivée, pas l'application
    pytesseract = None
    Image = None
    ImageOps = None

LANGS = "fra+deu"
MIN_WIDTH = 2000   # on agrandit les petites images
MAX_WIDTH = 3500   # on réduit les très grandes (vitesse)
ALLOWED_EXT = {".jpg", ".jpeg", ".png"}
MAX_BYTES = 15 * 1024 * 1024  # 15 Mo
WINDOWS_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]


class OCRError(Exception):
    """Lecture de photo impossible (message destiné à l'utilisateur)."""


def _setup() -> None:
    if pytesseract is None:
        raise OCRError("les paquets Python 'pytesseract' et 'pillow' ne sont pas installés")
    cmd = os.getenv("TESSERACT_CMD") or shutil.which("tesseract")
    if not cmd:
        cmd = next((p for p in WINDOWS_PATHS if Path(p).exists()), None)
    if not cmd:
        raise OCRError("Tesseract n'est pas installé sur cet ordinateur")
    pytesseract.pytesseract.tesseract_cmd = cmd
    try:
        available = set(pytesseract.get_languages(config=""))
    except Exception as e:  # noqa: BLE001
        raise OCRError(f"Tesseract ne répond pas ({e})") from e
    missing = [l for l in LANGS.split("+") if l not in available]
    if missing:
        raise OCRError(f"données de langue Tesseract manquantes : {', '.join(missing)}")


def preprocess(img):
    """Orientation du téléphone, niveaux de gris, contraste, taille adaptée."""
    img = ImageOps.exif_transpose(img)
    img = img.convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    if img.width < MIN_WIDTH:
        ratio = MIN_WIDTH / img.width
        img = img.resize((MIN_WIDTH, int(img.height * ratio)), Image.LANCZOS)
    elif img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
    return img


def image_to_text(image, psm: int = 6) -> tuple[str, float]:
    """Renvoie (texte, confiance moyenne 0-100). Lève OCRError si l'OCR est impossible."""
    _setup()
    if not hasattr(image, "convert"):  # tableau numpy
        image = Image.fromarray(image)
    img = preprocess(image)
    data = pytesseract.image_to_data(
        img, lang=LANGS, config=f"--oem 3 --psm {psm}", output_type=pytesseract.Output.DICT
    )
    lines, confs = {}, []
    for i, word in enumerate(data["text"]):
        word = word.strip()
        if not word:
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        lines.setdefault(key, []).append(word)
        try:
            c = float(data["conf"][i])
        except (TypeError, ValueError):
            continue
        if c >= 0:
            confs.append(c)
    text = "\n".join(" ".join(ws) for _, ws in sorted(lines.items()))
    return text, (sum(confs) / len(confs) if confs else 0.0)


def read_photo(image) -> tuple[str, str]:
    """Pour l'interface : (texte à placer dans la zone Courrier, message pour la personne)."""
    if image is None:
        return "", "Aucune image reçue."
    try:
        text, conf = image_to_text(image)
    except OCRError as e:
        return "", f"Lecture de la photo impossible : {e}."
    except Exception as e:  # noqa: BLE001
        return "", f"Lecture de la photo impossible ({type(e).__name__})."
    if not text.strip():
        return "", "Aucun texte lu. Essaie une photo plus nette, bien éclairée, prise à plat."
    if conf < 70:
        return text, (f"Photo difficile à lire (confiance {conf:.0f} %). "
                      "Relis TOUT le texte et corrige-le avant de continuer, surtout les montants et les dates.")
    return text, (f"Texte lu (confiance {conf:.0f} %). "
                  "Vérifie les montants et les dates avant de continuer : la lecture peut se tromper.")


def read_upload(path) -> tuple[str, str]:
    """Fichier téléversé -> (texte, message). Ne lève jamais d'exception."""
    if not path:
        return "", "Aucun fichier reçu."
    if Image is None:
        return "", "Lecture de la photo indisponible : pillow n'est pas installé."
    p = Path(path)
    if p.suffix.lower() not in ALLOWED_EXT:
        return "", "Format non pris en charge : utilise une image JPG, JPEG ou PNG."
    try:
        if p.stat().st_size > MAX_BYTES:
            return "", "Image trop lourde (maximum 15 Mo)."
        with Image.open(p) as img:
            img.load()  # force la lecture : détecte les fichiers corrompus
            return read_photo(img)
    except Exception:  # noqa: BLE001
        return "", "Fichier illisible : ce n'est pas une image valide."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python -m src.ocr chemin\\vers\\photo.jpg")
    img = Image.open(sys.argv[1])
    texte, message = read_photo(img)
    print(message, "\n")
    print(texte)