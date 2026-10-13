"""Enchaîne les étapes de Jisr : extraction -> recherche -> explication -> contrôle."""
import json
import re
import time

from pydantic import BaseModel, ValidationError, field_validator

from src.check import check_answer
from src.llm import call_llm
from src.prompts import (
    SYSTEM_PROMPT,
    build_explanation_prompt,
    build_extraction_prompt,
)

try:
    from src.retrieve import retrieve
except ImportError:  # retrieve.py n'est pas encore prêt (travail du Membre A)
    retrieve = None

# Passage de TEST uniquement (ce n'est pas une source officielle)
FAKE_PASSAGES = [
    {
        "id": "test_01",
        "texte": (
            "Passage de test : en cas de rappel de paiement, il faut payer le "
            "montant indiqué avant la date limite ou contester par écrit."
        ),
        "langue": "fr",
        "source_url": "test://passage-de-test",
        "theme": "test",
    }
]


class Extraction(BaseModel):
    type_document: str | None = None
    delai: str | None = None
    montant: str | None = None
    action_demandee: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def en_texte(cls, v):
        if v is None:
            return None
        return str(v).strip() or None


def parse_json(texte: str) -> dict:
    """Retire les ``` éventuels et isole le premier objet JSON."""
    texte = re.sub(r"```(?:json)?", "", texte).strip()
    debut, fin = texte.find("{"), texte.rfind("}")
    if debut == -1 or fin <= debut:
        raise ValueError("Aucun JSON trouvé dans la réponse du modèle")
    return json.loads(texte[debut : fin + 1])


def extract(courrier: str, model: str = "8b") -> tuple[dict, bool]:
    """Retourne (extraction, ok). Deux essais maximum."""
    prompt = build_extraction_prompt(courrier)
    for _ in range(2):
        brut = call_llm(
            prompt, model=model, system=SYSTEM_PROMPT, temperature=0.0, max_tokens=300
        )
        try:
            return Extraction(**parse_json(brut)).model_dump(), True
        except (ValueError, ValidationError):
            continue
    return Extraction().model_dump(), False


def get_passages(courrier: str, extraction: dict, k: int = 3):
    """Retourne (passages, avertissement ou None)."""
    if retrieve is None:
        return FAKE_PASSAGES, "retrieve.py indisponible : passage de test utilisé"
    requete = f"{extraction.get('type_document') or ''} {courrier[:500]}".strip()
    try:
        return retrieve(requete, k=k), None
    except Exception as e:  # noqa: BLE001
        return FAKE_PASSAGES, f"Recherche en échec ({e}) : passage de test utilisé"


def run_pipeline(courrier: str, model: str = "8b") -> dict:
    debut = time.perf_counter()
    avertissements = []

    extraction, extraction_ok = extract(courrier, model)
    if not extraction_ok:
        avertissements.append("Extraction JSON invalide : informations non fiables.")

    passages, alerte = get_passages(courrier, extraction)
    if alerte:
        avertissements.append(alerte)
    elif not passages:
        avertissements.append("Aucun passage officiel trouvé.")

    prompt = build_explanation_prompt(courrier, extraction, passages)
    reponse = call_llm(
        prompt, model=model, system=SYSTEM_PROMPT, temperature=0.3, max_tokens=900
    )

    controle = check_answer(extraction, reponse)
    if not controle["ok"]:
        avertissements.append(
            "Vérifiez les chiffres dans le courrier original : "
            + ", ".join(controle["manquants"])
        )

    return {
        "modele": model,
        "extraction": extraction,
        "extraction_ok": extraction_ok,
        "passages": passages,
        "reponse": reponse,
        "controle": controle,
        "avertissements": avertissements,
        "duree_s": round(time.perf_counter() - debut, 2),
    }