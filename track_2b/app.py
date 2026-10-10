"""Interface Gradio de Jisr."""
import html
import re

import gradio as gr

from src.llm import LLMError
from src.pipeline import run_pipeline

try:
    from src.ingest import ensure_index

    ensure_index()
except ImportError:
    print("ingest.py absent : démarrage sans index.")
except Exception as e:  # noqa: BLE001
    print(f"Indexation au démarrage échouée : {e}")

# ---------------------------------------------------------------- apparence
THEME = gr.themes.Soft(primary_hue="teal", secondary_hue="amber")

CSS = """
.gradio-container { max-width: 1150px !important; margin: 0 auto !important; }
#header { text-align: center; padding: 22px 0 8px; }
.header-title { font-size: 2.4rem; font-weight: 800; margin: 0; color: var(--primary-600); }
.header-sub { margin: 6px 0 0; color: var(--body-text-color-subdued); font-size: 1.05rem; }
.section-title { font-weight: 700; margin: 4px 0 8px; }
.answer { border: 1px solid var(--border-color-primary); background: var(--background-fill-secondary);
          border-radius: 14px; padding: 16px 20px; min-height: 220px; }
.answer p { margin: 0 0 10px; font-size: 1.2rem; line-height: 2; text-align: start;
            font-family: "Noto Naskh Arabic", "Segoe UI", Tahoma, Arial, sans-serif; }
.answer p.titre { font-weight: 700; color: var(--primary-600); margin-top: 14px; }
.answer.placeholder p { color: var(--body-text-color-subdued); font-style: italic; font-size: 1rem; }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 12px; }
.fact { border: 1px solid var(--border-color-primary); border-radius: 12px; padding: 10px 12px;
        background: var(--background-fill-primary); }
.fact span { display: block; font-size: .78rem; text-transform: uppercase; letter-spacing: .06em;
             color: var(--body-text-color-subdued); }
.fact b { font-size: 1.05rem; word-break: break-word; }
.badge { border-radius: 10px; padding: 10px 14px; font-weight: 600; margin-bottom: 8px; }
.badge.ok { background: #dcfce7; color: #166534; }
.badge.warn { background: #fef3c7; color: #92400e; }
.badge.err { background: #fee2e2; color: #991b1b; }
#footer { text-align: center; color: var(--body-text-color-subdued); font-size: .9rem; padding: 14px 0 4px; }
"""

HEADER = """
<div id="header">
  <p class="header-title">جسر &nbsp;·&nbsp; Jisr</p>
  <p class="header-sub">Colle un courrier officiel suisse (allemand ou français) :
  Jisr l'explique en darija, dit quoi faire, avant quand, et cite sa source.</p>
</div>
"""

FOOTER = """
<div id="footer">Jisr aide à comprendre un courrier. Il ne remplace pas un conseil juridique :
en cas de doute, contacte directement l'organisme qui a envoyé le courrier.</div>
"""

PLACEHOLDER = (
    '<div class="answer placeholder"><p dir="auto">L\'explication apparaîtra ici.</p></div>'
)

# Courriers de démonstration (inventés, volontairement différents de data/examples.txt)
EXEMPLES = {
    "Prime impayée": (
        "Rappel de prime\n"
        "Monsieur Exemple,\n"
        "Nous constatons que votre prime d'assurance de base de CHF 276.90 n'a pas été payée. "
        "Merci de régler ce montant d'ici au 12 décembre 2026. "
        "Sans paiement de votre part, une procédure de poursuite pourra être engagée."
    ),
    "Mahnung (allemand)": (
        "Mahnung\n"
        "Sehr geehrte Frau Beispiel\n"
        "Für die Rechnung Nr. 3190 haben wir bis heute keinen Zahlungseingang festgestellt. "
        "Bitte überweisen Sie den offenen Betrag von CHF 143.50 bis zum 3. Dezember 2026. "
        "Andernfalls müssen wir Mahngebühren erheben."
    ),
    "Obligation de s'assurer": (
        "Rappel d'affiliation\n"
        "Madame Exemple,\n"
        "Toute personne domiciliée en Suisse doit s'assurer pour les soins en cas de maladie. "
        "Nous n'avons pas reçu la preuve de votre assurance. "
        "Veuillez nous la transmettre d'ici au 31 décembre 2026."
    ),
}

# --------------------------------------------------------------- affichage
FACTS = [
    ("type_document", "Type"),
    ("delai", "Délai"),
    ("montant", "Montant"),
    ("action_demandee", "Action"),
]


def esc(valeur) -> str:
    return html.escape(str(valeur)) if valeur not in (None, "") else "—"


def badge(kind: str, texte: str) -> str:
    return f'<div class="badge {kind}">{html.escape(texte)}</div>'


def status_html(avertissements: list[str]) -> str:
    if not avertissements:
        return badge("ok", "✓ Contrôle des chiffres réussi")
    return "".join(badge("warn", f"⚠ {a}") for a in avertissements)


def answer_html(texte: str) -> str:
    """Un paragraphe par ligne ; dir="auto" choisit le sens de lecture (arabe : droite à gauche)."""
    paragraphes = []
    for ligne in texte.splitlines():
        ligne = re.sub(r"^[#>*\-\s]+", "", ligne).replace("**", "").strip()
        if not ligne:
            continue
        est_titre = len(ligne) <= 40 and ligne.endswith((":", "؟", "?"))
        classe = ' class="titre"' if est_titre else ""
        paragraphes.append(f'<p dir="auto"{classe}>{html.escape(ligne)}</p>')
    return f'<div class="answer">{"".join(paragraphes)}</div>'


def facts_html(extraction: dict) -> str:
    cases = "".join(
        f'<div class="fact"><span>{label}</span><b dir="auto">{esc(extraction.get(cle))}</b></div>'
        for cle, label in FACTS
    )
    return f'<div class="facts">{cases}</div>'


def sources_html(passages: list[dict]) -> str:
    if not passages:
        return "<p>Aucune source.</p>"
    items = ""
    for p in passages:
        url = p.get("source_url")
        suite = f" — {html.escape(url)}" if url else ""
        items += f"<li>{esc(p.get('id'))}{suite}</li>"
    return f"<ol>{items}</ol>"


# ---------------------------------------------------------------- logique
def analyser(courrier: str, modele: str):
    """Retourne (réponse, statut, cartes, sources, infos)."""
    if not courrier or not courrier.strip():
        return PLACEHOLDER, badge("warn", "Colle d'abord un courrier."), "", "", ""
    try:
        r = run_pipeline(courrier, model=modele)
    except LLMError as e:
        return PLACEHOLDER, badge("err", f"Erreur du modèle : {e}"), "", "", ""
    except Exception as e:  # noqa: BLE001 - on affiche l'erreur plutôt que de planter
        return PLACEHOLDER, badge("err", f"Erreur inattendue : {e}"), "", "", ""

    t = r.get("tokens") or {}
    tokens = f" · {t.get('prompt_tokens', 0)} + {t.get('completion_tokens', 0)} tokens" if t else ""
    infos = f"Apertus {r['modele']} · {r['duree_s']} s{tokens}"
    return (
        answer_html(r["reponse"]),
        status_html(r["avertissements"]),
        facts_html(r["extraction"]),
        sources_html(r["passages"]),
        infos,
    )


# ------------------------------------------------------------ interface
GR_MAJOR = int(gr.__version__.split(".")[0])
# Gradio 6 : thème et CSS se passent à launch() ; avant, à Blocks()
BLOCKS_KW = {} if GR_MAJOR >= 6 else {"theme": THEME, "css": CSS}
LAUNCH_KW = {"theme": THEME, "css": CSS} if GR_MAJOR >= 6 else {}

with gr.Blocks(title="Jisr · جسر", **BLOCKS_KW) as demo:
    gr.HTML(HEADER)

    with gr.Row():
        with gr.Column(scale=5):
            courrier = gr.Textbox(
                label="Courrier · الرسالة",
                placeholder="Colle ici le texte du courrier (allemand ou français)…",
                lines=14,
            )
            gr.HTML('<div class="section-title">Essayer un exemple</div>')
            with gr.Row():
                for nom, texte in EXEMPLES.items():
                    gr.Button(nom, size="sm").click(lambda t=texte: t, outputs=courrier)
            with gr.Row():
                bouton = gr.Button("Expliquer en darija", variant="primary", scale=3)
                effacer = gr.Button("Effacer", scale=1)
            with gr.Accordion("Options", open=False):
                modele = gr.Dropdown(choices=["8b", "70b"], value="8b", label="Modèle Apertus")

        with gr.Column(scale=5):
            statut = gr.HTML()
            gr.HTML('<div class="section-title">Explication · الشرح بالدارجة</div>')
            reponse = gr.HTML(PLACEHOLDER)
            faits = gr.HTML()
            with gr.Accordion("Sources et détails techniques", open=False):
                sources = gr.HTML()
                infos = gr.Markdown()

    gr.HTML(FOOTER)

    sorties = [reponse, statut, faits, sources, infos]
    bouton.click(analyser, inputs=[courrier, modele], outputs=sorties)
    effacer.click(
        lambda: ("", PLACEHOLDER, "", "", "", ""),
        outputs=[courrier, *sorties],
    )

demo.launch(server_name="0.0.0.0", server_port=7860, **LAUNCH_KW)