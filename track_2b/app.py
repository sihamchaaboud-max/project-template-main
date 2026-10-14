"""Interface Gradio de aji-tfhem : design « papier ivoire et or »."""
import html
import re

import gradio as gr

from src.llm import LLMError
from src.ocr import read_upload
from src.pipeline import run_pipeline

try:
    from src.ingest import ensure_index

    ensure_index()
except ImportError:
    print("ingest.py absent : démarrage sans index.")
except Exception as e:  # noqa: BLE001
    print(f"Indexation au démarrage échouée : {e}")

# ---------------------------------------------------------------- apparence
THEME = gr.themes.Base(
    primary_hue="amber",
    neutral_hue="stone",
    font=["system-ui", "Segoe UI", "Arial", "sans-serif"],
)

CSS = """
/* ---------- palette (clair / sombre) ---------- */
.gradio-container {
  --ivory:#f6f1e7; --paper:#fffdf8; --paper2:#f9f4ea; --ink:#1b2a41; --muted:#6a7383; --line:#e6dcc8;
  --gold:#b8893b; --goldsoft:#f3e6c8; --accent:#1b2a41; --on-accent:#fbf7ee;
  --ok-bg:#e4f1e8; --ok:#1f5f3a; --warn-bg:#faefd2; --warn:#7a5313; --err-bg:#f8e1df; --err:#8a2a22;
  --serif: Georgia, "Palatino Linotype", Palatino, "Book Antiqua", serif;
  --arabic: "Amiri", "Noto Naskh Arabic", "Traditional Arabic", "Segoe UI", Tahoma, serif;
  --body-background-fill: var(--ivory); --background-fill-primary: var(--paper);
  --background-fill-secondary: var(--paper2); --block-background-fill: var(--paper);
  --block-border-color: var(--line); --border-color-primary: var(--line);
  --body-text-color: var(--ink); --body-text-color-subdued: var(--muted);
  --block-label-text-color: var(--muted); --input-background-fill: var(--paper2);
  --input-border-color: var(--line); --input-background-fill-focus: var(--paper2);
  --button-primary-background-fill: var(--accent); --button-primary-background-fill-hover: var(--accent);
  --button-primary-text-color: var(--on-accent); --button-primary-border-color: var(--accent);
  --button-secondary-background-fill: transparent; --button-secondary-background-fill-hover: var(--goldsoft);
  --button-secondary-text-color: var(--ink); --button-secondary-border-color: var(--line);
  background: var(--ivory) !important; max-width: 100% !important; padding: 0 !important;
}
.dark .gradio-container {
  --ivory:#0d1520; --paper:#141f2d; --paper2:#101a27; --ink:#efe8d8; --muted:#97a1b0; --line:#25344a;
  --gold:#d6ab55; --goldsoft:#2a2a24; --accent:#d6ab55; --on-accent:#14202e;
  --ok-bg:#15382a; --ok:#b7e4c7; --warn-bg:#3a2f14; --warn:#f1d58a; --err-bg:#43201d; --err:#f5b8b2;
}
footer { display: none !important; }
#shell { max-width: 1180px; margin: 0 auto !important; padding: 28px 20px 0 !important; }

/* ---------- en-tête ---------- */
.top { border-bottom: 1px solid var(--line);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E%3Cg fill='none' stroke='%23b8893b' stroke-opacity='0.16' stroke-width='1'%3E%3Cpath d='M32 4 38 26 60 32 38 38 32 60 26 38 4 32 26 26Z'/%3E%3Ccircle cx='32' cy='32' r='7'/%3E%3C/g%3E%3C/svg%3E"),
    linear-gradient(180deg, var(--paper), var(--ivory)); }
.top-in { max-width: 1180px; margin: 0 auto; padding: 0 20px; }
.nav { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; padding: 18px 0; }
.brand { display: flex; align-items: baseline; gap: 12px; }
.brand-ar { font-family: var(--arabic); font-size: 1.8rem; font-weight: 700; color: var(--ink); }
.brand-lat { font-family: var(--serif); letter-spacing: .24em; text-transform: uppercase; font-size: .78rem; color: var(--gold); }
.powered { font-size: .85rem; color: var(--muted); }
.hero { display: grid; grid-template-columns: 1.5fr .5fr; gap: 24px; align-items: center; padding: 22px 0 38px; }
.eyebrow { margin: 0; color: var(--gold); text-transform: uppercase; letter-spacing: .2em; font-size: .78rem; font-weight: 700; }
.hero h1 { font-family: var(--serif); font-weight: 500; line-height: 1.1; letter-spacing: -.01em; color: var(--ink);
           font-size: clamp(2.2rem, 4.8vw, 3.5rem); margin: .25em 0 .4em; }
.hero h1 em { color: var(--gold); }
.lead { max-width: 560px; color: var(--muted); font-size: 1.1rem; margin: 0; }
.steps { list-style: none; display: flex; flex-wrap: wrap; gap: 10px 26px; padding: 0; margin: 22px 0 0; }
.steps li { display: flex; align-items: center; gap: 10px; font-size: .95rem; color: var(--ink); }
.steps b { width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid var(--gold); color: var(--gold);
           display: grid; place-items: center; font-size: .8rem; }
.arch { width: 100%; max-width: 220px; justify-self: center; color: var(--gold); }
@media (max-width: 820px) { .hero { grid-template-columns: 1fr; } .arch { display: none; } }

/* ---------- panneaux ---------- */
.panel { position: relative; background: var(--paper) !important; border: 1px solid var(--line) !important;
         border-radius: 22px !important; padding: 26px !important;
         box-shadow: 0 1px 2px rgba(27,42,65,.06), 0 14px 34px rgba(27,42,65,.08) !important; }
.panel::before { content: ""; position: absolute; inset-inline: 28px; top: -1px; height: 3px;
                 background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.panel .block { background: transparent !important; box-shadow: none !important; }
.panel-head { display: flex; align-items: baseline; justify-content: space-between;
              border-bottom: 1px solid var(--line); padding-bottom: 12px; margin-bottom: 14px; }
.panel-head h2 { margin: 0; font-family: var(--serif); font-weight: 500; font-size: 1.4rem; color: var(--ink); }
.panel-head .ar { font-family: var(--arabic); color: var(--gold); font-size: 1.3rem; }
.section-title { font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin: 14px 0 6px; }
#courrier { border: none !important; padding: 0 !important; }
#courrier textarea { background: var(--paper2) !important; border: 1px solid var(--line) !important;
                     border-radius: 14px !important; padding: 16px 18px !important; line-height: 1.7 !important;
                     font-size: 1rem !important; color: var(--ink) !important; }
#photo-file { border: 1.5px dashed var(--gold) !important; border-radius: 14px !important;
              background: var(--paper2) !important; }
button.primary { background: var(--accent) !important; color: var(--on-accent) !important; border: none !important;
                 border-radius: 999px !important; font-weight: 700 !important; letter-spacing: .02em !important;
                 padding: 12px 22px !important; transition: transform .15s, filter .15s; }
button.primary:hover { filter: brightness(1.15); transform: translateY(-1px); }
button.secondary { border-radius: 999px !important; background: transparent !important;
                   border: 1px solid var(--line) !important; color: var(--ink) !important; font-weight: 600 !important; }
button.secondary:hover { border-color: var(--gold) !important; color: var(--gold) !important; }
.chips button { font-size: .88rem !important; background: var(--paper2) !important; }
.privacy { font-size: .8rem; color: var(--muted); margin: 6px 0 0; }

/* ---------- résultat ---------- */
.badge { border-radius: 12px; padding: 10px 14px; font-weight: 600; margin-bottom: 10px; font-size: .95rem; }
.badge.ok { background: var(--ok-bg); color: var(--ok); }
.badge.warn { background: var(--warn-bg); color: var(--warn); }
.badge.err { background: var(--err-bg); color: var(--err); }
.type-pill { display: inline-block; background: var(--goldsoft); color: var(--gold); border-radius: 999px;
             padding: 4px 14px; font-size: .85rem; font-weight: 700; margin-bottom: 12px; }
.facts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 16px; }
.fact { border: 1px solid var(--line); border-top: 3px solid var(--gold); border-radius: 12px;
        padding: 12px 14px; background: var(--paper2); }
.fact span { display: block; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.fact b { font-family: var(--serif); font-size: 1.15rem; font-weight: 600; word-break: break-word; color: var(--ink); }
.answer { background: var(--paper2); border: 1px solid var(--line); border-radius: 14px;
          padding: 18px 22px; min-height: 210px; animation: rise .45s ease both; }
.answer.empty { color: var(--muted); font-style: italic; display: grid; place-items: center; text-align: center; animation: none; }
.answer.empty::before { content: "❖"; display: block; color: var(--gold); font-size: 1.6rem; font-style: normal; margin-bottom: 6px; }
.answer p { font-family: var(--arabic); font-size: 1.35rem; line-height: 2.05; margin: 0 0 8px; color: var(--ink); }
.answer p.titre { font-weight: 700; color: var(--gold); font-size: 1.2rem; margin-top: 16px;
                  padding-bottom: 4px; border-bottom: 1px dashed var(--line); }
.answer.empty p { font-family: inherit; font-size: 1rem; margin: 0; color: var(--muted); }
@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
#footer { max-width: 760px; margin: 36px auto 0; padding: 18px 20px 40px; text-align: center;
          color: var(--muted); font-size: .85rem; border-top: 1px solid var(--line); }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
"""

TOP = """
<div class="top"><div class="top-in">
  <div class="nav">
    <div class="brand"><span class="brand-ar">أجي تفهم</span><span class="brand-lat">aji-tfhem</span></div>
    <span class="powered">Propulsé par Apertus · modèle ouvert suisse 🇨🇭</span>
  </div>
  <div class="hero">
    <div>
      <p class="eyebrow">Courriers officiels suisses</p>
      <h1>Comprends ton courrier,<br><em>en darija.</em></h1>
      <p class="lead">Colle le texte ou envoie une photo. aji-tfhem t'explique ce que dit le courrier,
        ce que tu dois faire et avant quand, avec la source officielle.</p>
      <ol class="steps">
        <li><b>1</b>Colle ou photographie</li>
        <li><b>2</b>Lis l'explication en darija</li>
        <li><b>3</b>Agis à temps</li>
      </ol>
    </div>
    <svg class="arch" viewBox="0 0 200 260" fill="none" stroke="currentColor" aria-hidden="true">
      <path d="M20 250V110a80 80 0 0 1 160 0v140" stroke-width="2"/>
      <path d="M40 250V112a60 60 0 0 1 120 0v138" stroke-width="1.2" opacity=".7"/>
      <path d="M60 250V114a40 40 0 0 1 80 0v136" stroke-width="1" opacity=".5"/>
      <path d="M10 250H190" stroke-width="2"/>
      <path d="M100 40l6 14 15 2-11 10 3 15-13-8-13 8 3-15-11-10 15-2z" fill="currentColor" stroke="none" opacity=".85"/>
    </svg>
  </div>
</div></div>
"""

FOOTER = """
<div id="footer">aji-tfhem aide à comprendre un courrier. Il ne remplace pas un conseil juridique :
en cas de doute, contacte directement l'organisme qui a envoyé le courrier.</div>
"""

PLACEHOLDER = '<div class="answer empty"><p dir="auto">L\'explication apparaîtra ici.</p></div>'

COPY_JS = """() => {
  const el = document.querySelector('.answer:not(.empty)');
  if (!el) return;
  navigator.clipboard.writeText(el.innerText).then(() => {
    const t = document.createElement('div');
    t.textContent = '✓ Copié';
    t.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1b2a41;color:#fbf7ee;border:1px solid #b8893b;padding:10px 20px;border-radius:999px;font-weight:700;z-index:9999';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 1500);
  });
}"""


def panel_head(titre: str, arabe: str) -> str:
    return f'<div class="panel-head"><h2>{titre}</h2><span class="ar">{arabe}</span></div>'


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
TUILES = [("delai", "Délai"), ("montant", "Montant"), ("action_demandee", "À faire")]


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
    """« À retenir » : type de courrier, puis délai, montant et action."""
    pill = ""
    if extraction.get("type_document"):
        pill = f'<div class="type-pill" dir="auto">{esc(extraction["type_document"])}</div>'
    cases = "".join(
        f'<div class="fact"><span>{label}</span><b dir="auto">{esc(extraction.get(cle))}</b></div>'
        for cle, label in TUILES
    )
    return f'{pill}<div class="facts-grid">{cases}</div>'


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
def lire_photo(chemin):
    """Lit la photo avec src/ocr.py. Retourne (texte pour la zone Courrier, statut OCR)."""
    texte, message = read_upload(chemin)
    if not texte:
        # échec : on affiche l'erreur et on ne touche pas au texte déjà saisi
        return gr.update(), badge("err", message)
    # succès : le texte arrive dans la zone Courrier, sans message
    if message.startswith("Photo difficile"):
        return texte, badge("warn", message)
    return texte, ""


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

with gr.Blocks(title="aji-tfhem · أجي تفهم", **BLOCKS_KW) as demo:
    gr.HTML(TOP)

    with gr.Column(elem_id="shell"):
        with gr.Row(equal_height=False):
            # ----------------------------- panneau 1 : le courrier
            with gr.Column(scale=5, min_width=360, elem_classes="panel"):
                gr.HTML(panel_head("Ton courrier", "الرسالة"))
                with gr.Row(elem_classes="chips"):
                    boutons_exemples = [
                        (gr.Button(nom, size="sm"), texte) for nom, texte in EXEMPLES.items()
                    ]
                courrier = gr.Textbox(
                    show_label=False,
                    container=False,
                    elem_id="courrier",
                    placeholder="Colle ici le texte du courrier (allemand ou français). "
                                "Tu peux aussi corriger le texte lu sur une photo.",
                    lines=12,
                )
                gr.HTML('<div class="section-title">Ou une photo · صورة الرسالة</div>')
                photo = gr.File(
                    show_label=False,
                    elem_id="photo-file",
                    file_types=[".jpg", ".jpeg", ".png"],
                    type="filepath",
                )
                lire = gr.Button("Lire la photo", size="sm")
                ocr_statut = gr.HTML()
                with gr.Row():
                    bouton = gr.Button("Expliquer en darija", variant="primary", scale=3)
                    effacer = gr.Button("Effacer", scale=1)
                with gr.Accordion("Options", open=False):
                    modele = gr.Dropdown(choices=["8b", "70b"], value="8b", label="Modèle Apertus")
                gr.HTML('<p class="privacy">Rien n\'est enregistré : les photos sont lues puis supprimées.</p>')

            # ----------------------------- panneau 2 : l'explication
            with gr.Column(scale=5, min_width=360, elem_classes="panel"):
                gr.HTML(panel_head("Explication", "الشرح بالدارجة"))
                statut = gr.HTML()
                faits = gr.HTML()
                reponse = gr.HTML(PLACEHOLDER)
                copier = gr.Button("Copier l'explication", size="sm")
                with gr.Accordion("Sources et détails techniques", open=False):
                    sources = gr.HTML()
                    infos = gr.Markdown()

    gr.HTML(FOOTER)

    # ----------------------------- câblage
    for bouton_ex, texte_ex in boutons_exemples:
        bouton_ex.click(lambda t=texte_ex: t, outputs=courrier)

    sorties = [reponse, statut, faits, sources, infos]
    lire.click(lire_photo, inputs=photo, outputs=[courrier, ocr_statut])
    bouton.click(analyser, inputs=[courrier, modele], outputs=sorties)
    copier.click(fn=None, js=COPY_JS)
    effacer.click(
        lambda: ("", PLACEHOLDER, "", "", "", "", None, ""),
        outputs=[courrier, *sorties, photo, ocr_statut],
    )

demo.launch(server_name="0.0.0.0", server_port=7860, **LAUNCH_KW)