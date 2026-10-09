# Technical report — Jisr 

A deeper write-up than the README: what we built, how it works, and what the numbers say.
Passages marked **TO FILL** wait for a result or a decision that does not exist yet.

- **Track:** Track 2B — Own Project
- **Event:** Online
- **Team:** CHAABOUD Siham, CHERRADI Salma
- **Demo:** TO FILL (video link)

## 1. Summary

Many people of Moroccan origin living in Switzerland find official administrative mail hard to
understand, and missing a deadline has real consequences (for example the 10 days to object to a
payment order). **Jisr** reads an official Swiss letter (German or French) and explains it in
**Darija** (Moroccan Arabic): what it is about, what to do, by when, and which official source the
explanation relies on.

The pipeline is: field extraction from the letter by Apertus (JSON), retrieval of the closest
official passages (RAG), generation of the Darija explanation by Apertus, then a code check that
dates and amounts in the answer match the letter. Sources stay in German and French; only the
final answer is in Darija.

Scope: 3 letter categories (health insurance, payment reminder / debt enforcement, residence
permit), 22 federal law articles as the knowledge base, 20 synthetic letters for evaluation.

**Main result so far:** source retrieval puts an expected source in the top-3 for **81%** of the
letters (13 of 16): 100% for health insurance and residence, but only 50% for payment reminders.
Extraction, Darija generation and 8B vs 70B results: TO FILL.

## 2. Architecture

```
Letter (text, DE or FR)
   |
   v
[1] Extraction (Apertus)  -> JSON: categorie, type_document, delai, montant, action_demandee
   |
   v
[2] Retrieval (BGE-M3 + Chroma) -> 3 official law articles (FR/DE), one version per article
   |
   v
[3] Generation (Apertus)  -> short Darija explanation + glossary + source
   |
   v
[4] Check (code)          -> dates and amounts in the answer must appear in the letter
```

Components and files:
 
|         Step       |                File                          |                  Tool                    |
|--------------------|----------------------------------------------|------------------------------------------|
|  Source ingestion  |              `src/ingest.py`                 | Python, BGE-M3 (`BAAI/bge-m3`), ChromaDB |
|      Retrieval     |               `src/retrieve.py`              |          `retrieve(query, k=3)`          |
|     Model call     |               `src/llm.py`                   |                 TO FILL                  |
|       Prompts      |                `src/prompts.py`              |                 TO FILL                  |
| Pipeline and check |       `src/pipeline.py`, `src/check.py`      |                 TO FILL                  |
|     Interface      |                    `app.py`                  |                  Gradio                  |
|    Evaluation      | `eval/eval_retrieval.py`, `eval/run_eval.py` |                  Python                  |

Ingestion details: each source is split into passages of at most 900 characters (67 passages for
22 sources). Fedlex footnotes are removed and list markers are re-joined. The source title is
prepended to the indexed text. Embeddings are normalised and compared by cosine similarity.

Retrieval rule: `retrieve()` returns `k` **different** articles. If the same article shows up in
both French and German, only the best-ranked version is kept.

No-source rule: Jisr cites no official source if the extracted `type_document` is `autre`
(other), or if the best retrieval score is below 0.54.

### Target architecture (mandatory)

- **Established:** retrieval (BGE-M3 and Chroma) runs **entirely locally, with no network**, once
  the model is downloaded (tested with `HF_HUB_OFFLINE=1`). The sources are text files in the
  repository. This part sends no data to any external service.
- **To establish:** where Apertus runs (local weights or a hosted service). This decides which
  architecture we can claim:
  - local Apertus weights, no network call at runtime: **a) on-premise** and **b) air-gapped**
    are defensible;
  - Apertus hosted in Switzerland: **c) sovereign Swiss cloud**, to be specified (operator,
    jurisdiction, data residency);
  - Apertus hosted outside Switzerland: none of the three would hold, and the report must say so.

**Build time (network needed):** installing Python packages, downloading BGE-M3 (about 2.3 GB)
from Hugging Face, downloading Apertus weights if used locally, collecting the sources from
Fedlex.

**Runtime (no network if Apertus is local):** indexing (`python -m src.ingest`), retrieval,
extraction, generation, check, Gradio interface.

**External dependencies:** TO FILL.

## 3. Use of Apertus

- **Model:** TO FILL (exact identifiers, for example `swiss-ai/Apertus-...`, 8B and 70B if
  access is simple).
- **How it is used:** inference (JSON extraction and generation of the Darija explanation). No
  fine-tuning.
- **Where it runs:** TO FILL (local weights or hosted endpoint, hardware, quantisation).
- **Parameters:** `temperature = 0` so that the benchmark is reproducible.
- **Prompts:** the extraction prompt used in `eval/run_eval.py` is **provisional**; the reference
  version is in `src/prompts.py`.
- **Darija strategy:** TO FILL (result of the 10-sentence test; escalation: examples, glossary,
  example base; fallback: simple standard Arabic).

## 4. Data

**Knowledge base: 22 files, 3 federal laws, in French and German.**

|                  Category                   |   Law (RS number)    |      Articles       |
|---------------------------------------------|----------------------|---------------------|
|    `assurance_maladie` (health insurance)   | LAMal / KVG (832.10) | art. 3, 64, 64a, 65 |
| `rappel_poursuite` (reminder / enforcement) | LP / SchKG (281.1)   |   art. 67, 69, 74   |
|           `sejour` (residence)              | LEI / AIG (142.20)   |art. 12, 33, 34, 62  |

- Every article exists in a French and a German version (suffix `_de`), copied **verbatim**,
  without rewording. Each file has a header (`id`, `titre`, `source`, `url`, `langue`, `theme`,
  `date_acces`).
- Source: Fedlex (fedlex.admin.ch), accessed on 2026-10-08. The LAMal texts are the version in
  force since 1 January 2026.
- **Licence:** federal laws are official acts, which are in principle not protected by Swiss
  copyright (art. 5 CopA). The source is cited. TO VERIFY: Fedlex terms of use.
- **URL check:** TO DO. The Fedlex addresses in the headers must be opened one by one to confirm
  that they lead to the right law.

**Test set: 20 synthetic letters** (`data/testset.json`), written by hand for this project. No
real document and no personal data: names, numbers, addresses, amounts and dates are invented.

|       Category         | Letters |  Language  |
|------------------------|---------|------------|
|   `rappel_poursuite`   |    6    | 3 FR, 3 DE |
|  `assurance_maladie`   |    5    | 2 FR, 3 DE |
|        `sejour`        |    5    | 3 FR, 2 DE |

Each letter has `date_courrier`, `langue`, an `attendu` (expected: document type, deadline
`YYYY-MM-DD`, amount as a number or `null`, requested action) and `source_ids_attendus`
(expected sources). Conventions: `delai` = the nearest deadline the person must meet; `montant` =
the total to pay if it is written, otherwise the main debt; FR and DE versions of the same
article count as the same source.

No data comes from real people, so there is no consent question for the data. Darija quality
ratings will be given by a native speaker: TO FILL (who, how, consent).

## 5. Evaluation

**Method.** Two benchmarks. `eval/eval_retrieval.py` measures retrieval alone: the query is the
letter text, and a hit@3 is counted if an expected source is among the 3 returned articles.
`eval/run_eval.py` measures extraction (category, deadline, amount), citation and latency.
`type_document` is not scored as an exact match (free-text labels), and `action_demandee` is
reviewed by hand. `autre` letters are excluded from retrieval scores.

### 5.1 Retrieval alone (measured)

16 letters with an expected source (the 4 `autre` letters have none).

|                   Setup                     |     hit@3       | recall@3 | MRR  |
|---------------------------------------------|-----------------|----------|------|
|   Query = full letter (retained method)     | **81%** (13/16) |    81%   | 0.77 |
| Query = expected type and action (`oracle`) |   75% (12/16)   |    75%   | 0.58 |

By category (query = full letter):

|       Category      | n | hit@3 | MRR  |
|---------------------|---|-------|------|
| `assurance_maladie` | 5 | 100%  | 1.00 |
|       `sejour`      | 5 | 100%  | 0.87 |
| `rappel_poursuite`  | 6 | 50%   | 0.50 |

By language: German 75% (n = 8), French 88% (n = 8). With 8 letters per language, this gap
cannot be interpreted.

**FR/DE deduplication.** On the first 15 letters the score is identical with and without
deduplication (87%). The gain is qualitative: the top-3 holds three different articles instead of
two articles repeated in both languages.

**The `oracle` query is not a clean upper bound.** It is built from `action_demandee`, written in
French even for German letters. It only shows that this reformulation does not help; it does not
show that extraction would not help retrieval.

**The 3 failures** (t05, t06, t20) are first reminders from a creditor threatening enforcement.
The expected source is art. 67 LP (request for enforcement), but retrieval returns art. 69 and 74
(payment order and objection). Art. 67 is indexed correctly: a short query such as "Réquisition de
poursuite que doit faire le créancier" ranks it first (score 0.714). The full letter (amounts,
invoice numbers, polite phrases) drowns that signal. Note: choosing art. 67 as the expected source
is debatable, since art. 69 and 74 describe what is likely to follow for the recipient of the
reminder. The test set was not modified after seeing the results.

**"No official source" threshold.** Best retrieval score: from 0.557 to 0.777 for letters with a
source (mean 0.663), from 0.468 to 0.523 for the 4 `autre` letters. A threshold of 0.54 separates
all of them, with a margin of 0.03. Caveats: only 4 out-of-scope letters, a threshold chosen on the
same data that evaluates it, synthetic letters. With the `oracle` query the separation disappears.

### 5.2 Extraction, citation and generation: TO FILL

The script `eval/run_eval.py` is ready and was tested with a fake model (no number from that test
is a result). The rows below will be filled with real Apertus outputs.

|            Setup           | Valid JSON | Category | Exact deadline | Exact amount | Citation | Latency |
|----------------------------|------------|----------|----------------|--------------|----------|---------|
|  Apertus 8B, no glossary   |            |          |                |              |          |         |
| Apertus 8B, with glossary  |            |          |                |              |          |         |
| Apertus 70B, no glossary   |            |          |                |              |          |         |
| Apertus 70B, with glossary |            |          |                |              |          |         |

Note: the "citation" column mixes retrieval quality and extraction quality (a wrong `autre`
category blocks any citation). It must be read together with section 5.1.

### 5.3 Darija quality and cost: TO FILL

- Darija quality rating by a native speaker (meaning, real Darija vs standard Arabic,
  administrative terms, numbers intact).
- Cost per request: latency measured by `run_eval.py`; token or compute consumption to be logged
  in `src/llm.py`. TO FILL.

## 6. Limitations

- **Narrow knowledge base:** 22 law articles from 3 domains. No plain-language pages (ch.ch, SEM,
  cantonal offices). Letters outside these domains cannot be sourced; the system must say so.
- **Payment reminders:** retrieval poorly surfaces the request for enforcement (50%). This
  category lacks sources written in everyday language.
- **Small, synthetic test set:** 20 letters written by the same team as the system, so cleaner
  than real letters (no scans, no OCR, no typos). 8 letters per language for retrieval: gaps
  between languages are not significant.
- **Fragile 0.54 threshold:** margin of 0.03 on 4 out-of-scope letters.
- **Displayed passage:** for a given source, the returned passage is not always the most useful
  one (for example paragraph 7 of art. 64a LAMal instead of paragraph 1). The cited source is
  correct, but the text handed to the generator may miss the essential part.
- **Laws, not practice:** Jisr cites law articles, not office practice or cantonal rules. Exact
  deadlines for some procedures are in ordinances absent from the base (for example the arrival
  declaration deadline, in the OASA).
- **Not legal advice:** to be displayed clearly in the interface.
- **Darija:** low-resource language, no single writing convention. TO FILL (observed limits).
- **Not tested:** real letters, scans, other cantons, other national languages.

## 7. Reproducibility

- **Environment:** Python 3.13, Windows, laptop, VS Code. GPU: TO CONFIRM (indexing 67 passages
  takes about 1 minute on the development machine).
- **Install:** `pip install -r requirements.txt`
- **Indexing:** `python -m src.ingest` (22 files, 67 passages). The `data/chroma/` folder is not in
  Git; it is rebuilt with this command.
- **Retrieval:** `python -m eval.eval_retrieval` (retained method) and
  `python -m eval.eval_retrieval --query oracle`. Results in `eval/results_retrieval_*.md`.
- **Extraction:** `python -m eval.run_eval --model 8b` (then `70b`). `--fake` is only for testing
  the script.
- **Determinism:** retrieval is deterministic. For models, `temperature = 0`. Seed: TO FILL.
- **Offline mode:** `HF_HUB_OFFLINE=1` once the models are downloaded.
- **Exact version:** commit TO FILL. `make run`: TO FILL (check against the `Makefile`).

## 8. Next steps

- Add ch.ch and SEM plain-language pages for each category, and publish a measured before/after
  (first for payment reminders).
- Add implementing ordinances (OASA for the arrival declaration deadline).
- Grow the test set (at least 50 letters, with scans and OCR) and have part of it written by
  someone outside the team.
- Evaluate passage size (500, 900, 1,500 characters) on a larger test set.
- Reformulate the query with the extraction (document type and action, in the letter's language).
- Example base in Darija validated by native speakers.
- More categories: taxes, schooling, employment.

## License

Creative Commons Attribution 4.0 (CC-BY-4.0). All HackApertus projects are open-sourced.

## References

- Fedlex, systematic collection of federal law: LAMal (RS 832.10), LP (RS 281.1), LEI (RS 142.20).
- BGE-M3: `BAAI/bge-m3` (Hugging Face).
- ChromaDB: vector database.
- Apertus: TO FILL (model reference).
