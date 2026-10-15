# Technical report: aji-tfhem

- **Track:** Track 2B (Own Project)
- **Event:** Online
- **Team:** CHAABOUD Siham, CHERRADI Salma (ENSA Al Hoceima, software engineering)
- **Demo:** TO FILL (video link)

## 1. Summary

Official letters in German or French use legal vocabulary and carry deadlines with legal consequences, for example 10 days to object to a payment order (art. 74 SchKG). People who read neither language well, such as Darija speakers recently arrived in Switzerland, may struggle to understand them. We did not survey users: this motivation is an assumption, not a measured need.

**aji-tfhem** (Darija for "come and understand") takes the text of an official Swiss letter and explains it in Darija: what it says, what to do, by when, and which official source supports the explanation. Apertus extracts the key fields as JSON, a retrieval step (RAG) finds the closest passages of 3 federal laws, Apertus writes the Darija explanation using a glossary and examples, and a code check verifies that the extracted numbers appear in the answer. Sources stay in German and French; only the final answer is in Darija.

**Headline results (20 synthetic letters, single runs):** the right law article is among the top 3 retrieved for 88% of letters (14/16). With the team prompt, Apertus 8B returns valid JSON for 100% of letters, the exact amount for 95% and the exact deadline for 85%. With few-shot examples, both models answer in Arabic script with Darija markers. **The main weakness we measured is source citation:** about one answer in four cites a wrong article. The quality of the Darija has not yet been rated by a native speaker.

|                              Component                         |                    Status                    |
|----------------------------------------------------------------|----------------------------------------------|
|        Source ingestion and retrieval (BGE-M3, ChromaDB)       |           Implemented, evaluated             |
| Extraction and generation with Apertus 8B and 70B (remote API) | Implemented, evaluated with automatic checks |
|                     Number check (`check.py`)                  |      Implemented, limited (section 6)        |
|                         Gradio interface                       |    Implemented; runs locally and in Docker   |
|                                      Docker                    | Image builds and the server starts; end-to-end run from a fresh clone not yet confirmed |
|                Native-speaker rating of Darija                 |                   Not done                   |
|       OCR of photos (Tesseract, French and German)             | Prototype module and synthetic test script; not in the interface, not evaluated |
|                    Audio input, fine-tuning                    |                Not implemented               |

## 2. Architecture

```
Letter text (DE or FR)
  -> [1] Extraction (Apertus, JSON: type, deadline, amount, action)
  -> [2] Retrieval (BGE-M3 + ChromaDB): 3 distinct law articles
  -> [3] Generation (Apertus): Darija explanation, glossary, examples, source
  -> [4] Check (code): extracted numbers must appear in the answer
  -> Gradio interface (explanation + 4 summary cards + disclaimer)
  (photo -> Tesseract -> text: prototype, not connected)
```

|   Step    |      File         |                                                 Details                                          |
|-----------|-------------------|--------------------------------------------------------------------------------------------------|
| Ingestion | `src/ingest.py`   | 22 files, 67 passages of at most 900 characters; Fedlex footnotes removed, footnote digits glued to article numbers removed; law title prepended to each passage; index built at startup by `ensure_index()` if absent |
| Retrieval | `src/retrieve.py` | BGE-M3 embeddings (`BAAI/bge-m3`), cosine similarity in ChromaDB; returns k=3 distinct articles (a French and a German version of the same article count once) |
| Model call| `src/llm.py`      | HTTPS POST to an OpenAI-compatible `/chat/completions` endpoint; endpoint, key and model names come from environment variables; 2 retries, 120 s timeout |
| Prompts   | `src/prompts.py`  | system prompt; extraction prompt (copy dates and amounts verbatim, null if absent); explanation prompt with a 47-entry Darija glossary and `data/examples.txt` (examples written by a native speaker, per the project documentation) |
| Pipeline  | `src/pipeline.py` | extraction (JSON validated with Pydantic, 2 attempts, temperature 0), retrieval with query = document type + first 500 characters, generation (temperature 0.3), check |
| Check     | `src/check.py`    | every number of the extracted amount and deadline must appear in the answer (Arabic-Indic digits are normalised) |
| Interface | `app.py`          | Gradio; header, example letters, warnings, four cards (type, deadline, amount, action), legal disclaimer |

Retrieved passages are placed in the prompt and the model is told to rely only on the letter and these passages. This grounds the answer but does not prevent unsupported statements, as sections 5 and 6 show.

### Target architecture (mandatory)

- **Runs locally:** embeddings (BGE-M3), vector store (ChromaDB), OCR prototype, check and interface. After the first download, retrieval works with `HF_HUB_OFFLINE=1`.
- **Runs remotely:** Apertus inference, through the HTTPS endpoint configured in `APERTUS_BASE_URL`. **Where this endpoint is hosted, and under which jurisdiction: TO FILL.**
- **Consequence:** we claim no architecture for the complete system until this is confirmed. If the endpoint is operated by the organisation deploying the system, architecture (a) on-premise applies; if it is hosted in Switzerland under Swiss jurisdiction with Swiss data residency, (c) sovereign Swiss cloud applies; otherwise none of the three holds and the system would need locally served Apertus weights. Because the model call is a standard chat-completions request, a locally served Apertus exposing the same API could replace the endpoint by changing environment variables. **This substitution has not been tested**, and no air-gapped deployment has been demonstrated.
- **Data handling:** only the letter text is sent to the model endpoint; the remote provider's retention policy is outside our control (TO FILL).
- **Build time vs runtime:** the image installs PyTorch (CPU) and the Python dependencies at build time (11 min 44 s on our connection). BGE-M3 (about 2.3 GB) is currently downloaded on first use at runtime, not during the build, so the first request after a fresh start is slow.

## 3. Use of Apertus

- **Models:** Apertus 8B and 70B, both called through the API. **Exact model identifiers (values of `APERTUS_MODEL_8B` and `APERTUS_MODEL_70B`): TO FILL.**
- **Role:** (1) extraction of type, deadline, amount and action as JSON (temperature 0, at most 300 tokens); (2) explanation in Darija from the letter, the extraction, the retrieved passages, the glossary and the examples (temperature 0.3 in the application, 0 in our evaluation, at most 900 tokens). No fine-tuning.
- **Why Apertus:** it is the model family required by the track and an open Swiss model. Whether it handles Darija is what we measured, not an assumption.
- **Darija strategy:** examples and glossary in the prompt. Without the examples, the 70B answered in French or Modern Standard Arabic (7% Arabic script, section 5.3).
- **Latency measured** from our development machine to the remote endpoint: extraction 1.0 to 1.3 s (8B) and 1.8 to 2.0 s (70B); generation 1.8 to 2.6 s (8B) and 3.5 to 4.2 s (70B) per request.

## 4. Data

**Knowledge base: 22 text files (about 61 KB), 3 federal laws, French and German,** copied verbatim from Fedlex (accessed 2026-10-08; LAMal in the version in force since 1 January 2026). Each file has a header (`id`, `titre`, `source`, `url`, `langue`, `theme`, `date_acces`).

|          Category              |            Law          |   Articles     |
|--------------------------------|-------------------------|----------------|
|          health insurance      | LAMal / KVG (RS 832.10) | 3, 64, 64a, 65 |
| payment reminder / enforcement |   LP / SchKG (RS 281.1) | 67, 69, 74     |
|         residence              |   LEI / AIG (RS 142.20) | 12, 33, 34, 62 |

Federal laws are official acts, in principle not protected by Swiss copyright (art. 5 CopA); the source is cited. The Fedlex terms of use and the header URLs still have to be verified. The size of the whole `data/` directory (the local index is rebuilt and not committed) has to be checked against the 100 MB limit.

**Test set: 20 synthetic letters** (`data/testset.json`), written by hand: 6 payment reminders, 5 health insurance, 5 residence, 4 out of scope; 10 French and 10 German. Names, numbers and amounts are invented; no real document and no personal data. Each letter has an expected type, deadline (`YYYY-MM-DD`), amount (number or null), action and expected sources. Convention: the deadline is the nearest one the person must meet.

## 5. Evaluation

**Method.** Single runs on the 20 synthetic letters, written by the team that built the system, so they are cleaner than real letters. Dates and amounts are normalised by the evaluation code (the team prompt copies dates as written). Extraction and generation runs used the pipeline version before the ingestion fix and before the latest prompt changes; the retrieval figures are after the fix. These runs are to be repeated once for the final version (TO UPDATE). One letter is worth 5 points, so gaps of one or two letters are not significant.

### 5.1 Retrieval (measured)

Query = full letter text; success (hit@3) if an expected source is among the 3 returned articles; 16 letters have an expected source.

|    Category      | n |     hit@3       | MRR  |
|------------------|---|-----------------|------|
| health insurance | 5 |      100%       | 1.00 |
|   residence      | 5 |      100%       | 0.87 |
| payment reminder | 6 |      67%        | 0.56 |
|    **All**       | 16| **88% (14/16)** | 0.79 |

French letters 100% (n=8), German 75% (n=8); this gap is not interpretable with so few letters. Before cleaning the footnote digits in the passages, the result was 81% (13/16), so one letter changed; we did not tune anything on the test set. The two failures (t06, t20) are first reminders from a creditor: the expected art. 67 SchKG is indexed but art. 69, 74 and 64a LAMal rank higher with the full letter as query. A query built from the expected extraction did not help (75% on the earlier index).

**"No official source" threshold.** With the full letter as query, letters with a source scored 0.548 to 0.777 and the 4 out-of-scope letters 0.468 to 0.523, so a threshold of 0.54 separates them, with a margin of 0.025 on 4 letters. With the pipeline's own query (document type + first 500 characters), one legitimate letter scored 0.5391 against 0.532 for the best out-of-scope letter: the threshold is fragile.

### 5.2 Extraction (measured, Apertus, 20 letters)

|                Prompt                             | Model | Valid JSON | Category | Exact deadline | Exact amount | Citation* | Latency |
|---------------------------------------------------|-------|------------|----------|----------------|--------------|-----------|---------|
|      v1: team pipeline (verbatim copy)            | 8B    |   100%     |    n/a   |       85%      |      95%     |    85%    | 1.0 s   |
|          v2: category + ISO dates                 | 8B    |   100%     |   75%    |       85%      |      90%     |    85%    | 1.2 s   |
| v3: written after reading the errors (optimistic) | 8B    |   100%     |   85%    |       85%      |      100%    |    85%    | 1.2 s   |
|                       v1                          | 70B   |   100%     |   n/a    |       85%      |      95%     |    85%    | 1.8 s   |
|                       v3                          | 70B   |   100%     |   80%    |       85%      |      95%     |    85%    | 2.0 s   |

*Citation: expected source in the top 3 and, for out-of-scope letters, no source cited (category "other" or score below 0.54). It mixes retrieval and extraction quality.

- **8B and 70B perform the same on this task** (all gaps are one letter) and the 70B is about 1.7 times slower.
- **The same three payment-order letters fail with every model and prompt:** the models return the 20-day payment deadline instead of the 10-day objection deadline, even when the prompt states that the earliest deadline must be chosen.
- **Amounts:** the prompt that asks for a "total" (v2) made the model add costs that are not written in the letter (3,553.30 instead of 3,480.00); copying verbatim (v1) avoids this. The only 8B error with v1 is letter t10, where the model picked the total treatment cost (1,850) instead of the 455 to pay.
- **Out-of-scope letters:** the 8B classifies 0 to 1 of 4 as out of scope (v2, v3), the 70B 2 of 4 (v3). The 100% citation score on these letters comes from the score threshold, not from the model.

### 5.3 Generation (automatic checks; native-speaker rating TO FILL)

Extraction and passages are fixed per letter and shared by three variants; temperature 0; when the best score is below 0.54, no passage is given. "Correct / wrong / none" counts answers whose cited article number is in / not in the expected sources / that cite no article (letters with passages and an expected source: 16 for the 8B, 15 for the 70B).

| Model |      Variant        | check.py | Amount in answer | Arabic script | Article correct / wrong / none | Latency |
|-------|---------------------|----------|------------------|---------------|--------------------------------|---------|
| 8B    | glossary + examples |  100%    |       100%       |      89%      |       11 / 4 / 1               | 2.3 s   |
| 8B    |   examples only     |  100%    |       100%       |      89%      |       10 / 4 / 2               | 2.1 s   |
| 8B    |    neither          |  90%     |       94%        |      92%      |        0 / 0 / 16              | 1.8 s   |
| 70B   | glossary + examples |  95%     |       100%       |      88%      |        7 / 3 / 5               | 4.2 s   |
| 70B   |   examples only     |  90%     |       100%       |      86%      |        5 / 1 / 9               | 4.0 s   |
| 70B   |       neither       |  95%     |       100%       |      7%       |        0 / 0 / 15              | 3.5 s   |

- **The examples make the model write in Darija script.** Without them, the 70B answers in French or Modern Standard Arabic.
- **The glossary has no visible effect on these automatic checks.** Its effect on Darija quality is not measured. We observed one glossary-related error (70B, letter t15: a fee translated as a health-insurance contribution).
- **Wrong citations (one in four for the 8B).** Causes found: an irrelevant passage retrieved for reminders (art. 64a LAMal), footnote digits glued to article numbers ("Art. 65264", fixed in ingestion), and the law name missing from the passage (fixed). A prompt rule "cite a passage only if it applies directly" is a remaining fix. The 8B once cited an article for an out-of-scope letter.
- **Deadline line:** the answers explain both the 20-day and the 10-day deadlines in the text, but the "by when" line gives a duration from the notification date, not a calendar date. The date appears in only 85% of answers for every variant, because of the three payment orders above.
- **Check limitations:** `check.py` compares the extraction with the answer, not with the letter, so it cannot catch a wrong extraction that the answer repeats; a number written in words (e.g. "twenty") counts as missing (one false alarm, letter t01).

### 5.4 Not evaluated

Native-speaker rating of the Darija (meaning, real Darija vs standard Arabic, terminology, numbers intact): TO FILL. OCR: a prototype exists (`src/ocr.py`, `eval/run_ocr.py`, which renders the test letters as degraded synthetic images), with no result reported.

## 6. Limitations

- **Narrow knowledge base:** 22 articles from 3 laws, no plain-language pages, no ordinances; letters outside these domains cannot be sourced.
- **Citation reliability:** about one wrong cited article in four (measured on the version before the fixes). For a legal-information tool this is the main risk; users must verify against the official source.
- **Relative deadlines:** the 10-day objection deadline of a payment order is not selected by any model or prompt tested, and the answer does not give the calendar date.
- **Fragile no-source rule:** margin below 0.03; the models detect out-of-scope letters poorly; the rule is not part of the production pipeline in the version we evaluated.
- **Evaluation:** 20 synthetic letters, single runs, prompt v3 tuned on the same letters, automatic checks only, Darija quality unrated, no real or scanned letters.
- **Remote dependency:** generation needs Internet access and an API key; latency and data retention depend on the provider; the Docker image downloads BGE-M3 at first use; the Docker engine had 3.5 GB of memory by default on our machine.
- **Not legal advice:** the interface displays a disclaimer.

## 7. Reproducibility

- **Run:** `track_2b/Makefile` defines `run` (creates `.env` from `.env.example` if missing, then `docker compose up --build`); the interface listens on port 7860. The `.env` file needs `APERTUS_BASE_URL`, `APERTUS_API_KEY`, `APERTUS_MODEL_8B` and `APERTUS_MODEL_70B`. **How judges obtain credentials: TO FILL. Invocation from the repository root and a fresh-clone run: TO CONFIRM.**
- **Local alternative:** `pip install -r requirements.txt`, `python app.py` (the index is built at first start). Developed on Windows with Python 3.13; the Docker image uses Python 3.11.
- **Evaluation commands (from `track_2b/`):** `python -m eval.eval_retrieval`, `python -m eval.run_eval --model 8b` (options `--extractor eval|v3`, `--model 70b`), `python -m eval.run_generation --model 8b`, `python -m eval.score_sources --model 8b`. Results are in `eval/`.
- **Determinism:** retrieval is deterministic; evaluation uses temperature 0, the application uses 0.3 for generation. Hardware: laptop CPU; indexing 67 passages takes about 1 minute. Commit: TO FILL.

## 8. Next steps and conclusion

- Add the prompt rule on citations and re-run the evaluation on the final version, with fresh letters never used to tune a prompt.
- Extract every deadline separately and compute calendar dates in code; apply a softer no-source rule (show the passage with a warning).
- Add plain-language pages (ch.ch, SEM) and the implementing ordinances; publish a measured before/after for payment reminders.
- Rate the Darija with native speakers, with and without the glossary; add a check against the letter text, not only the extraction.
- Integrate and evaluate the OCR on real photographs of printed fictional letters, with an editable text step; serve Apertus locally to demonstrate an on-premise deployment.

**Conclusion.** aji-tfhem is a working prototype: retrieval over three federal laws, extraction and Darija generation with Apertus, an interface and a Docker image. Our measurements show that the extraction is reliable on clean synthetic letters and that the 8B is sufficient, but that source citation and relative deadlines are not yet reliable enough for unsupervised use, and that Darija quality and the deployment architecture remain to be validated.

## License

Creative Commons Attribution 4.0 (CC-BY-4.0). All HackApertus projects are open-sourced.

## References

- Fedlex, systematic collection of Swiss federal law: LAMal (RS 832.10), LP (RS 281.1), LEI (RS 142.20). https://www.fedlex.admin.ch
- Apertus model family (Swiss AI Initiative): TO FILL (exact model card URLs and versions).
- Chen et al., BGE M3-Embedding, 2024 (arXiv 2402.03216); model `BAAI/bge-m3` on Hugging Face.
- ChromaDB: https://www.trychroma.com
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- Gradio: https://www.gradio.app ; Docker: https://docs.docker.com
