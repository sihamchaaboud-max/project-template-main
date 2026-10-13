"""
eval/run_eval.py : benchmark principal de aji-tfhem (extraction + chiffres + citation)

Extracteurs (--extractor) :
  pipeline : le VRAI pipeline de B (src/pipeline.py : extract + get_passages). Défaut.
             Pas de champ "categorie" dans son extraction : catégorie non notée.
  eval     : prompt v2 de ce fichier (categorie + dates AAAA-MM-JJ), via call_llm.
  v3       : prompt v3 (délai qui expire en premier, montant recopié sans addition, "autre").
             ATTENTION : v3 a été écrit APRÈS avoir lu les erreurs sur ces 20 courriers.
             Ses scores sont optimistes ; à confirmer sur des courriers jamais vus.
  --fake   : faux modèle avec erreurs volontaires (test du script).

Notes par courrier :
  json_ok    : extraction exploitable
  categorie  : catégorie extraite == attendue (modes eval et v3)
  delai      : date exacte après normalisation ("9. November 2026", "15.10.2026",
               "1er mai 2026" acceptés)
  montant    : nombre exact après normalisation ("CHF 1'250.-" -> 1250.0) ;
               null attendu -> null obtenu
  citation   : courrier avec source : une source attendue est dans le top-3 ;
               courrier "autre" : aji-tfhem ne cite rien (type/categorie "autre" OU score < SEUIL).
               NB : le pipeline de B n'applique pas encore cette règle.

Non noté : type_document, action_demandee (relecture à la main), qualité de la darija.
Le parseur JSON tolère l'échappement invalide \\' (observé sur le 8B).

Usage (depuis track_2b/) :
    python -m eval.run_eval --fake
    python -m eval.run_eval --model 8b --limit 3
    python -m eval.run_eval --model 8b
    python -m eval.run_eval --model 8b --extractor eval
    python -m eval.run_eval --model 8b --extractor v3
    python -m eval.run_eval --model 70b
"""
import argparse
import json
import re
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTSET = ROOT / "data" / "testset.json"
SEUIL_SOURCE = 0.54  # sous ce score du meilleur passage : "pas de source officielle"

EVAL_PROMPT = """Tu lis un courrier officiel suisse (allemand ou français).
Réponds UNIQUEMENT avec un objet JSON, sans texte autour, avec ces clés :
- "categorie" : une valeur parmi "assurance_maladie", "rappel_poursuite", "sejour", "autre"
- "type_document" : court, en minuscules avec underscores (ex. "commandement_de_payer")
- "delai" : la date limite la plus proche que la personne doit respecter, au format AAAA-MM-JJ.
  Si le délai est relatif (« dans les dix jours »), calcule-le à partir de la date de notification
  ou de la date du courrier. null s'il n'y a aucun délai.
- "montant" : le montant total à payer en CHF s'il est écrit, sinon le montant principal,
  comme nombre (ex. 1250.00). null s'il n'y a aucun montant.
- "action_demandee" : ce que la personne doit faire, en une phrase.

Date du courrier : {date_courrier}

Courrier :
\"\"\"
{courrier}
\"\"\"
"""

V3_PROMPT = """Tu lis un courrier officiel suisse (allemand ou français).
Réponds UNIQUEMENT avec un objet JSON valide, sans texte autour, avec ces clés :
- "categorie" : "assurance_maladie", "rappel_poursuite" ou "sejour" si le courrier relève
  clairement de ce domaine ; sinon "autre" (par exemple impôts, banque, contrat de travail,
  ou tout autre sujet).
- "type_document" : court, en minuscules avec underscores.
- "delai" : la date limite, au format AAAA-MM-JJ.
  * Si le courrier donne plusieurs délais, choisis celui qui expire EN PREMIER
    (par exemple, un délai d'opposition de 10 jours expire avant un délai de paiement de 20 jours).
  * Si le délai est relatif (« dans les dix jours »), calcule la date à partir de la date de
    notification écrite dans le courrier, sinon à partir de la date du courrier.
  * null s'il n'y a aucun délai.
- "montant" : le montant en CHF que la personne doit payer (ou qu'elle reçoit), recopié tel qu'il
  est écrit dans le courrier, comme nombre (ex. 1250.00). Ne fais JAMAIS d'addition toi-même et
  n'invente aucun chiffre. null s'il n'y a aucun montant.
- "action_demandee" : ce que la personne doit faire, en une phrase.

Date du courrier : {date_courrier}

Courrier :
\"\"\"
{courrier}
\"\"\"
"""

PROMPTS = {"eval": EVAL_PROMPT, "v3": V3_PROMPT}

MONTHS = {
    # français
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
    "décembre": 12, "decembre": 12,
    # allemand
    "januar": 1, "jänner": 1, "februar": 2, "märz": 3, "maerz": 3, "juni": 6, "juli": 7,
    "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12,
}


def normalize_date(x):
    """Renvoie 'AAAA-MM-JJ' ou None si la date n'est pas reconnue."""
    if x is None:
        return None
    s = str(x).strip().lower()
    if not s:
        return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m[1]}-{m[2]}-{m[3]}"
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", s)
    if m:
        return f"{int(m[3]):04d}-{int(m[2]):02d}-{int(m[1]):02d}"
    m = re.search(r"(\d{1,2})(?:er|\.)?\s*([a-zäéûèôç]+)\s+(\d{4})", s)
    if m and m[2] in MONTHS:
        return f"{int(m[3]):04d}-{MONTHS[m[2]]:02d}-{int(m[1]):02d}"
    return None


def to_number(x):
    """Renvoie un float, None (absent) ou 'invalide'."""
    if x is None:
        return None
    s = str(x).lower()
    s = re.sub(r"chf|sfr|fr\.|francs?", "", s)
    s = s.replace("'", "").replace("’", "").replace(" ", "").replace("\u00a0", "")
    s = re.sub(r"[-–—]+$", "", s).rstrip(".")
    if re.fullmatch(r"\d+,\d{1,2}", s):
        s = s.replace(",", ".")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return "invalide"


def parse_json(text):
    if not isinstance(text, str):
        return None
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    a, b = text.find("{"), text.rfind("}")
    if a == -1 or b <= a:
        return None
    candidate = text[a : b + 1].replace("\\'", "'")  # \' est invalide en JSON
    try:
        obj = json.loads(candidate)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def norm(source_id: str) -> str:
    return source_id[:-3] if source_id.endswith("_de") else source_id


def fake_extract(t: dict, i: int) -> str:
    """Faux modèle : l'attendu avec des erreurs volontaires (test du script)."""
    att = t["attendu"]
    out = {"categorie": t["categorie"], "type_document": att["type_document"],
           "delai": att["delai"], "montant": att["montant"],
           "action_demandee": att["action_demandee"]}
    if i == 6:
        return "Désolé, je ne peux pas répondre en JSON."
    if i % 4 == 3 and out["montant"] is not None:
        out["montant"] = out["montant"] + 20
    if i % 5 == 4:
        out["delai"] = "2026-10-01"
    if i % 7 == 5:
        out["categorie"] = "autre"
    return "```json\n" + json.dumps(out, ensure_ascii=False) + "\n```"


def main(model: str, extractor: str, fake: bool, limit) -> None:
    tests = json.loads(TESTSET.read_text(encoding="utf-8"))
    if limit:
        tests = tests[:limit]

    mode = "fake" if fake else extractor
    if mode == "pipeline":
        from src.pipeline import extract as pipeline_extract, get_passages
    else:
        from src.retrieve import retrieve
        if mode in PROMPTS:
            from src.llm import call_llm

    rows, raws = [], []
    for i, t in enumerate(tests):
        print(f"{t['id']} ...", flush=True)
        att = t["attendu"]
        got, raw, passages, warn, erreur = None, None, [], None, None

        # --- 1. extraction
        t0 = time.time()
        try:
            if mode == "fake":
                raw = fake_extract(t, i)
                got = parse_json(raw)
            elif mode in PROMPTS:
                prompt = PROMPTS[mode].format(date_courrier=t["date_courrier"], courrier=t["courrier"])
                raw = call_llm(prompt, model=model, temperature=0.0, max_tokens=300)
                got = parse_json(raw)
            else:
                got, ok = pipeline_extract(t["courrier"], model)
                raw = json.dumps(got, ensure_ascii=False)
                if not ok:
                    got = None
        except Exception as e:  # noqa: BLE001  (une erreur d'API ne doit pas tout arrêter)
            erreur = f"{type(e).__name__}: {e}"
        latence = time.time() - t0

        # --- 2. recherche
        try:
            if mode == "pipeline":
                passages, warn = get_passages(t["courrier"], got or {})
            else:
                passages = retrieve(t["courrier"], k=3)
        except Exception as e:  # noqa: BLE001
            erreur = (erreur or "") + f" | recherche: {e}"
        top_ids = [norm(p["id"]) for p in passages]
        top_score = passages[0].get("score", 0.0) if passages else 0.0

        # --- 3. notes
        row = {"id": t["id"], "categorie": t["categorie"], "langue": t["langue"],
               "latence_s": round(latence, 2), "json_ok": int(got is not None),
               "montant_attendu": att["montant"], "erreur": int(erreur is not None),
               "warn": int(warn is not None)}
        if got is not None:
            row["cat_ok"] = int(got.get("categorie") == t["categorie"]) if "categorie" in got else None
            row["delai_ok"] = int(normalize_date(got.get("delai")) == att["delai"])
            g_m, a_m = to_number(got.get("montant")), att["montant"]
            row["montant_ok"] = (int(g_m is None) if a_m is None
                                 else int(isinstance(g_m, float) and abs(g_m - float(a_m)) < 0.005))
            predit_autre = (got.get("categorie") == "autre"
                            or str(got.get("type_document") or "").lower() == "autre")
        else:
            row.update(cat_ok=(None if mode == "pipeline" else 0), delai_ok=0, montant_ok=0)
            predit_autre = False

        ne_cite_rien = predit_autre or top_score < SEUIL_SOURCE
        expected = [norm(s) for s in t["source_ids_attendus"]]
        if t["categorie"] == "autre":
            row["citation_ok"] = int(ne_cite_rien)
        else:
            row["citation_ok"] = int(any(s in top_ids for s in expected) and not ne_cite_rien)
        rows.append(row)
        raws.append({"id": t["id"], "extraction": got, "sortie_brute": raw, "attendu": att,
                     "top3": top_ids, "top_score": top_score, "avertissement": warn,
                     "erreur": erreur})

    # --- agrégation
    def pct(rs, key):
        vals = [r[key] for r in rs if r.get(key) is not None]
        return f"{sum(vals) / len(vals):.0%}" if vals else "n/a"

    titres = {"fake": "FAKE (test du script, ces chiffres ne sont PAS des résultats)",
              "pipeline": f"pipeline de B, Apertus {model}",
              "eval": f"prompt v2 (categorie + ISO), Apertus {model}",
              "v3": f"prompt v3 (écrit après lecture des erreurs : scores optimistes), Apertus {model}"}
    L = [f"# Benchmark extraction + citation : {titres[mode]}\n",
         f"Courriers : {len(rows)}. Seuil de source : {SEUIL_SOURCE}.\n",
         "## Global\n",
         f"- JSON exploitable : **{pct(rows, 'json_ok')}**",
         f"- Catégorie : **{pct(rows, 'cat_ok')}**",
         f"- Délai exact : **{pct(rows, 'delai_ok')}**",
         f"- Montant exact : **{pct(rows, 'montant_ok')}**",
         f"- Citation correcte : **{pct(rows, 'citation_ok')}**",
         f"- Latence moyenne d'extraction : {sum(r['latence_s'] for r in rows) / len(rows):.2f} s",
         f"- Erreurs d'appel : {sum(r['erreur'] for r in rows)} ; "
         f"recherche de secours (passage de test) : {sum(r['warn'] for r in rows)}\n"]

    for champ, nom in (("categorie", "Par catégorie"), ("langue", "Par langue")):
        g = defaultdict(list)
        for r in rows:
            g[r[champ]].append(r)
        L += [f"## {nom}\n",
              f"| {champ} | n | JSON | catégorie | délai | montant | citation |",
              "|---|---|---|---|---|---|---|"]
        for k, rs in sorted(g.items()):
            L.append(f"| {k} | {len(rs)} | {pct(rs, 'json_ok')} | {pct(rs, 'cat_ok')} | "
                     f"{pct(rs, 'delai_ok')} | {pct(rs, 'montant_ok')} | {pct(rs, 'citation_ok')} |")
        L.append("")

    avec = [r for r in rows if r["montant_attendu"] is not None]
    sans = [r for r in rows if r["montant_attendu"] is None]
    L += ["## Montant : avec et sans montant dans le courrier\n",
          f"- Courriers avec montant ({len(avec)}) : {pct(avec, 'montant_ok')}",
          f"- Courriers sans montant, `null` attendu ({len(sans)}) : {pct(sans, 'montant_ok')}\n",
          "## Détail\n",
          "| id | catégorie | JSON | catég. | délai | montant | citation |",
          "|---|---|---|---|---|---|---|"]

    def ok(v):
        return "n/a" if v is None else ("OK" if v else "RATE")
    for r in rows:
        L.append(f"| {r['id']} | {r['categorie']} | {ok(r['json_ok'])} | {ok(r['cat_ok'])} | "
                 f"{ok(r['delai_ok'])} | {ok(r['montant_ok'])} | {ok(r['citation_ok'])} |")

    tag = "fake" if fake else f"{model}_{extractor}"
    out_md = ROOT / "eval" / f"results_extraction_{tag}.md"
    out_json = ROOT / "eval" / f"raw_extraction_{tag}.json"
    out_md.write_text("\n".join(L), encoding="utf-8")
    out_json.write_text(json.dumps(raws, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(L))
    print(f"\n(écrit dans {out_md} et {out_json})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="8b", choices=["8b", "70b"])
    ap.add_argument("--extractor", default="pipeline", choices=["pipeline", "eval", "v3"])
    ap.add_argument("--fake", action="store_true", help="faux modèle, pour tester le script")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    main(a.model, a.extractor, a.fake, a.limit)