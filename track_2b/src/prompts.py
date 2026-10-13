"""Consignes (prompts) de Jisr : du texte et des assemblages, aucune logique métier."""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SYSTEM_PROMPT = (
    "Tu es Jisr, un assistant qui aide des personnes parlant la darija marocaine "
    "à comprendre des courriers officiels suisses. Tu es fiable, clair et prudent. "
    "Tu n'inventes jamais une information."
)

EXTRACTION_PROMPT = """Tu lis un courrier officiel suisse.
Réponds UNIQUEMENT avec un objet JSON, sans texte avant ou après, avec exactement ces clés :
{{"type_document": "", "delai": "", "montant": "", "action_demandee": ""}}

Règles :
- Recopie la date et le montant exactement comme dans le courrier.
- Si une information est absente, mets null.
- N'invente rien.

COURRIER :
{courrier}
"""

EXPLANATION_PROMPT = """Tu aides une personne qui parle la darija marocaine à comprendre un courrier suisse.

RÈGLES :
1. Écris en darija marocaine simple (écriture arabe), avec des phrases courtes.
2. Appuie-toi UNIQUEMENT sur le courrier et sur les passages officiels ci-dessous.
   Si une information manque, dis-le clairement.
3. Recopie les dates et les montants EXACTEMENT comme dans les données extraites.
   Ne les traduis pas et ne les arrondis pas.
4. Garde les termes officiels importants (nom d'un formulaire ou d'un organisme)
   dans leur langue d'origine, entre parenthèses, après l'explication en darija.
5. Utilise ce glossaire quand un terme y figure :
{glossaire}

FORMAT DE LA RÉPONSE (titres en darija) :
- Ce que dit le courrier (2 phrases maximum)
- Ce que tu dois faire
- Avant quand
- Source : le nom ou le lien du passage utilisé
- Dernière phrase : en cas de doute, contacte directement l'organisme qui a envoyé le courrier.

EXEMPLES DU STYLE ATTENDU :
{exemples}

DONNÉES EXTRAITES DU COURRIER :
{extraction}

PASSAGES OFFICIELS :
{passages}

COURRIER :
{courrier}
"""


def load_glossary(path: Path | None = None) -> list[dict]:
    path = path or DATA_DIR / "glossary.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def format_glossary(entries: list[dict]) -> str:
    """Garde seulement les termes dont la traduction darija est remplie."""
    lignes = [
        f"- {e.get('fr') or e.get('de')} → {e['darija']}"
        for e in entries
        if e.get("darija")
    ]
    return "\n".join(lignes) or "(aucun terme)"


def load_examples(path: Path | None = None) -> str:
    """Exemples de bonnes réponses en darija, écrits par une locutrice native."""
    path = path or DATA_DIR / "examples.txt"
    try:
        texte = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        texte = ""
    return texte or "(aucun exemple)"


def format_passages(passages: list[dict]) -> str:
    if not passages:
        return "(aucun passage trouvé)"
    blocs = []
    for i, p in enumerate(passages, start=1):
        source = p.get("source_url") or p.get("id", "")
        blocs.append(f"[{i}] (source : {source})\n{p['texte']}")
    return "\n\n".join(blocs)


def build_extraction_prompt(courrier: str) -> str:
    return EXTRACTION_PROMPT.format(courrier=courrier.strip())


def build_explanation_prompt(
    courrier: str,
    extraction: dict,
    passages: list[dict],
    glossaire: list[dict] | None = None,
) -> str:
    if glossaire is None:
        glossaire = load_glossary()
    return EXPLANATION_PROMPT.format(
        glossaire=format_glossary(glossaire),
        exemples=load_examples(),
        extraction=json.dumps(extraction, ensure_ascii=False),
        passages=format_passages(passages),
        courrier=courrier.strip(),
    )