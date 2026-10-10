"""Contrôle simple (sans IA) : les dates et montants du courrier sont-ils dans la réponse ?"""
import re

# Chiffres arabes-indiens (٠١٢...) et persans (۰۱۲...) -> chiffres 0-9
CHIFFRES = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


def normaliser(texte: str) -> str:
    return texte.translate(CHIFFRES)


def _nombres(texte: str) -> list[str]:
    return re.findall(r"\d+(?:[.,'’]\d+)*", normaliser(texte))


def _variantes(nombre: str) -> set[str]:
    sans_apostrophe = nombre.replace("'", "").replace("’", "")
    variantes = {nombre, sans_apostrophe, nombre.replace(",", ".")}
    if re.fullmatch(r"\d+[.,]00", sans_apostrophe):
        variantes.add(sans_apostrophe[:-3])  # "240.00" accepté aussi comme "240"
    return variantes


def check_answer(extraction: dict, reponse: str) -> dict:
    """Vérifie que chaque nombre du montant et du délai figure dans la réponse."""
    reponse_norm = normaliser(reponse)
    manquants = []
    for champ in ("montant", "delai"):
        valeur = extraction.get(champ)
        if not valeur:
            continue
        for nombre in _nombres(valeur):
            trouve = any(
                re.search(rf"(?<!\d){re.escape(v)}(?!\d)", reponse_norm)
                for v in _variantes(nombre)
            )
            if not trouve:
                manquants.append(f"{champ} : {nombre}")
    return {"ok": not manquants, "manquants": manquants}