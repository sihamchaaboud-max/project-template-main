"""
eval/run_ocr.py : robustesse de la lecture de photos (OCR) sur les 20 courriers synthétiques.

Chaque courrier est rendu en image, puis dégradé de plusieurs façons (rotation, flou, JPEG de
mauvaise qualité, ombre et bruit, petite taille). On lit l'image avec src/ocr.py et on mesure :
  similarite    : ressemblance du texte lu avec le texte d'origine (0-100 %, SequenceMatcher)
  montant_ok    : le montant attendu est lu exactement (comparaison des chiffres seuls, donc
                  "1'250.00" et "1 250.00" comptent pareil) ; courriers avec montant seulement
  nombres_ok    : part des nombres du courrier (2 chiffres ou plus) retrouvés dans le texte lu

LIMITE IMPORTANTE : ce sont des images SYNTHÉTIQUES (texte net rendu par ordinateur, puis dégradé).
Elles sont plus faciles que de vraies photos (plis, reflets, perspective, papier froissé).
Ce test mesure la sensibilité de l'OCR à quelques dégradations, pas sa performance réelle.
Pour un chiffre plus honnête : photographier 5 courriers synthétiques imprimés avec un téléphone.

Usage (depuis track_2b/) :
    python -m eval.run_ocr --limit 3
    python -m eval.run_ocr
"""
import argparse
import io
import json
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from eval.run_generation import nums
from src.ocr import OCRError, image_to_text

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"
CONDITIONS = ["propre", "tourne", "flou", "petit", "jpeg", "ombre_bruit"]
FONTS = [r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def load_font(size: int):
    for f in FONTS:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def render(text: str, width: int = 1240, margin: int = 80, size: int = 30) -> Image.Image:
    font = load_font(size)
    probe = ImageDraw.Draw(Image.new("RGB", (width, 10)))
    max_w = width - 2 * margin
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            test = (cur + " " + w).strip()
            if probe.textlength(test, font=font) <= max_w:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    line_h = int(size * 1.5)
    img = Image.new("RGB", (width, margin * 2 + line_h * len(lines)), "white")
    d, y = ImageDraw.Draw(img), margin
    for line in lines:
        d.text((margin, y), line, fill="black", font=font)
        y += line_h
    return img


def degrade(img: Image.Image, cond: str) -> Image.Image:
    if cond == "propre":
        return img
    if cond == "tourne":
        return img.rotate(3, expand=True, fillcolor="white", resample=Image.BICUBIC)
    if cond == "flou":
        return img.filter(ImageFilter.GaussianBlur(1.5))
    if cond == "petit":
        return img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
    if cond == "jpeg":
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=20)
        buf.seek(0)
        return Image.open(buf).convert("RGB")
    if cond == "ombre_bruit":
        arr = np.asarray(img.convert("L"), dtype=float)
        arr = arr * np.linspace(1.0, 0.65, arr.shape[1])[None, :]
        arr = arr + np.random.default_rng(0).normal(0, 14, arr.shape)
        return Image.fromarray(np.clip(arr, 0, 255).astype("uint8")).convert("RGB")
    raise ValueError(cond)


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main(limit) -> None:
    tests = json.loads(TESTSET.read_text(encoding="utf-8"))
    if limit:
        tests = tests[:limit]

    rows, echecs = [], []
    for t in tests:
        original = t["courrier"]
        base = render(original)
        wanted = {n for n in nums(original) if len(re.sub(r"\D", "", n)) >= 2}
        montant = t["attendu"]["montant"]
        for cond in CONDITIONS:
            print(f"{t['id']} / {cond} ...", flush=True)
            try:
                text, conf = image_to_text(degrade(base, cond))
            except OCRError as e:
                raise SystemExit(f"OCR impossible : {e}")
            row = {"id": t["id"], "cond": cond, "conf": conf,
                   "sim": SequenceMatcher(None, squash(original), squash(text)).ratio()}
            got = nums(text)
            row["nombres"] = (len(wanted & got) / len(wanted)) if wanted else None
            if montant is not None:
                digits = re.sub(r"\D", "", text)
                row["montant"] = int(re.sub(r"\D", "", f"{montant:.2f}") in digits)
                if not row["montant"]:
                    echecs.append(f"- {t['id']} / {cond} : montant {montant:.2f} non retrouvé")
            else:
                row["montant"] = None
            rows.append(row)

    def mean(vals, pct=True):
        vals = [v for v in vals if v is not None]
        if not vals:
            return "n/a"
        m = sum(vals) / len(vals)
        return f"{m:.0%}" if pct else f"{m:.0f}"

    L = [f"# Lecture de photos (OCR) : {len(tests)} courriers, rendus en images synthétiques\n",
         "Moteur : Tesseract 'fra+deu' (local). Images synthétiques dégradées : plus faciles que de "
         "vraies photos. À compléter par un test sur de vraies photos de courriers fictifs imprimés.\n",
         "| Condition | n | similarité | montant exact | nombres exacts | confiance Tesseract |",
         "|---|---|---|---|---|---|"]
    for cond in CONDITIONS:
        r = [x for x in rows if x["cond"] == cond]
        L.append(f"| {cond} | {len(r)} | {mean([x['sim'] for x in r])} | "
                 f"{mean([x['montant'] for x in r])} | {mean([x['nombres'] for x in r])} | "
                 f"{mean([x['conf'] for x in r], pct=False)} |")
    L += ["", "## Montants non retrouvés\n"] + (echecs or ["(aucun)"])
    out = ROOT / "eval" / "results_ocr.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n(écrit dans {out})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    main(ap.parse_args().limit)