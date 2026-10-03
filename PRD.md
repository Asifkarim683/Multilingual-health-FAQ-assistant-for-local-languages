# Product Requirements Document: Multilingual Health FAQ Assistant

Version 1.1 | Status: Draft | Type: Portfolio project (AI/ML engineering)

Changes in 1.1: added multi-language expansion (section 4.3), a language registry, per-language evaluation gates, and GitHub parts 10 and 11 for onboarding new languages.

---

## 1. Overview

A web-based assistant that answers general health questions in Hindi, Odia, and English at launch (v1), built so that more Indian languages can be added in later releases (v1.1 and v2) through configuration. Answers are generated only from trusted public health sources (WHO, Indian government health bodies) and always include a citation. If the answer is not in the sources, the assistant refuses and suggests seeing a doctor.

The assistant provides information only. It does not diagnose, prescribe, or give dosage advice.

### 1.1 Problem statement

Most reliable health information is published in English. Many people in India, especially in smaller cities and rural areas, are more comfortable in Hindi, Odia, or other local languages. General chatbots answer in these languages but often hallucinate medical facts and give no sources. Users cannot tell whether an answer is safe.

### 1.2 Solution summary

A retrieval-augmented generation (RAG) system with:
- A curated, multilingual knowledge base built from public sources.
- Cross-lingual retrieval, so a Hindi or Odia question can match an English source passage.
- Answers generated strictly from retrieved passages, with citations.
- A refusal path for out-of-scope, unsafe, or unsupported questions.
- A measured evaluation on a hand-labeled test set.

### 1.3 Why this project (portfolio value)

- Narrow user and real constraint: low-resource language, high-stakes domain.
- Shows safety thinking: refusals, citations, disclaimers.
- Measured results, not just a demo.
- Full-stack delivery: data pipeline, ML, API, UI, deployment.

---

## 2. Goals and Non-goals

### 2.1 Goals

| ID | Goal | Measure |
|----|------|---------|
| G1 | Answer common health questions in Hindi, Odia, English | Answer relevance rated 4/5 or higher on 80% of test questions |
| G2 | Ground every answer in a source | 100% of answers include at least one citation |
| G3 | Retrieve the right passage across languages | Recall@5 of 85% or higher on the test set |
| G4 | Avoid unsupported claims | Faithfulness of 90% or higher (claims supported by retrieved text) |
| G5 | Refuse correctly | 90% or higher of out-of-scope or unsafe test questions are refused |
| G6 | Be usable | Response time under 8 seconds at p95; works on a mobile screen |
| G7 | Add a language without code changes | New language onboarded by adding a registry entry, sources, and eval data only |
| G8 | Be honest about per-language quality | Results published per language; failing languages labeled experimental |

### 2.2 Non-goals (v1)

- Diagnosis, treatment plans, or medication dosing.
- Handling personal medical records or any user health data.
- Voice input and output (planned for v2).
- Languages beyond Hindi, Odia, English in v1 (added in v1.1 and v2, see section 4.3).
- Emergency triage or replacing medical professionals.

---

## 3. Users and Use Cases

### 3.1 Primary personas

1. **Asha, 45, homemaker, Odia-speaking.** Wants to know what to do about a child's fever, which foods to avoid with high blood pressure. Reads Odia comfortably, English poorly.
2. **Ravi, 28, shopkeeper, Hindi-speaking.** Wants to understand vaccination schedules and common seasonal illnesses (dengue, malaria).
3. **Reviewer persona (recruiter or engineer).** Wants to see a live demo, a clear README, evaluation numbers, and clean code in under 5 minutes.

### 3.2 Core user stories

- As a user, I can type a question in my language and get an answer in the same language.
- As a user, I can see which source the answer came from and open it.
- As a user, I am told clearly when the assistant does not know, and what to do next.
- As a user, I see a short disclaimer that this is information, not medical advice.
- As a user, I can switch the interface language.
- As a user, I can give a thumbs up or down on an answer.
- As a developer, I can run the evaluation suite and see metrics in one command.

### 3.3 Example interactions

| Question | Expected behavior |
|----------|-------------------|
| "What are the symptoms of dengue?" (Hindi) | Answer in Hindi from WHO/NVBDCP source with citation |
| "How many times should a child get the polio vaccine?" (Odia) | Answer in Odia from immunization schedule source with citation |
| "Which tablet should I take for chest pain?" | Refuse dosage/medication advice; urge urgent care |
| "I have chest pain and trouble breathing" | Emergency message: seek immediate medical help, no further generation |
| "Who won the cricket match?" | Out-of-scope refusal |
| Question on a topic not in the knowledge base | "I could not find this in my sources" plus doctor suggestion |

---

## 4. Scope

### 4.1 Topic coverage (v1)

Keep the scope narrow so quality can be measured. Suggested set of 8 topics:

1. Dengue, malaria, and other vector-borne diseases
2. Diabetes basics and lifestyle
3. Hypertension basics and lifestyle
4. Child immunization schedule
5. Maternal health and pregnancy care basics
6. Nutrition and anemia
7. Hygiene, water safety, diarrhea and ORS
8. Seasonal illnesses (flu, fever when to seek care)

### 4.2 Languages

| Language | Role | Notes |
|----------|------|-------|
| English | Source language for most documents | Used as base for the knowledge base |
| Hindi | Question and answer language | Many official documents available in Hindi |
| Odia | Question and answer language | Lowest-resource; document where quality is weaker |

### 4.3 Language expansion plan

| Release | Languages | Initial status |
|---------|-----------|----------------|
| v1 | English, Hindi, Odia | Stable once the onboarding checklist passes |
| v1.1 | Bengali, Telugu, Tamil (default plan; change here and in the registry if different) | Experimental until the checklist passes |
| v2 | Marathi, Gujarati, Kannada, Malayalam, Punjabi | Experimental until the checklist passes |

**Language registry.** Each language is one entry in `config/languages.yaml`. The pipeline, API, and UI read from it, so adding a language does not require code changes.

```yaml
languages:
  - code: or
    name: Odia
    native_name: ଓଡ଼ିଆ
    script: Odia
    font: Noto Sans Oriya
    status: stable            # stable | experimental
    emergency_keywords: []    # reviewed by a native speaker
    disclaimer: ""
    example_questions: []
    eval_file: data/eval/or.csv
```

**Onboarding checklist (applies to every new language).**

| Step | Pass condition |
|------|----------------|
| Sources collected and listed in `SOURCES.md` | At least 3 documents covering the core topics; usage terms checked |
| Registry entry complete | Emergency keywords, disclaimer, and UI strings present and native-speaker reviewed |
| Evaluation data | 50 questions plus 10 refusal cases, with gold passages |
| Retrieval | Recall@5 within 10 points of English |
| Faithfulness | 90% or higher on the language's test set |
| Language match | 98% or higher of answers in the question's language |
| Refusal accuracy | 90% or higher on the language's refusal set |
| Rendering | Script displays correctly at 360 px width |

**Status rules.** A language that passes every step is marked `stable`. A language that fails any step ships as `experimental`, shown with a visible label in the UI, and its numbers are published in the README. A language is never marked `stable` without native-speaker review of its emergency keywords.

---

## 5. Functional Requirements

### 5.1 Chat and answering

| ID | Requirement | Priority |
|----|-------------|----------|
| F1 | Accept a text question in Hindi, Odia, or English | Must |
| F2 | Detect the question language automatically, with manual override | Must |
| F3 | Retrieve top-k relevant passages using multilingual embeddings | Must |
| F4 | Generate the answer only from retrieved passages, in the user's language | Must |
| F5 | Return citations (document title, section or page, link) with every answer | Must |
| F6 | Refuse when retrieval confidence is below a threshold | Must |
| F7 | Detect emergency keywords and show an emergency message instead of an answer | Must |
| F8 | Detect medication-dosage or diagnosis requests and refuse | Must |
| F9 | Show a disclaimer on every answer | Must |
| F10 | Maintain short conversation context (last 3 turns) for follow-ups | Should |
| F11 | Thumbs up/down feedback stored with the question ID | Should |
| F12 | Show the original English source text alongside the translated answer | Could |
| F13 | Load supported languages, keywords, disclaimers, and UI strings from `config/languages.yaml` | Must |
| F14 | Show an "experimental" label on answers in languages not yet marked stable | Must |

### 5.2 Knowledge base management

| ID | Requirement | Priority |
|----|-------------|----------|
| K1 | Ingest PDFs and HTML pages from a source list | Must |
| K2 | Clean and chunk text with metadata (source, language, topic, URL, date) | Must |
| K3 | Store embeddings in a vector database | Must |
| K4 | Re-run ingestion with one command | Must |
| K5 | Maintain a `SOURCES.md` listing every source and its license/terms | Must |
| K6 | Report chunk counts and topic coverage per language after each ingestion | Must |

### 5.3 Evaluation

| ID | Requirement | Priority |
|----|-------------|----------|
| E1 | Hand-labeled test set of at least 150 questions (50 per language) | Must |
| E2 | Automated retrieval metrics: Recall@k, MRR | Must |
| E3 | Answer quality checks: faithfulness, citation correctness | Must |
| E4 | Refusal test set (at least 30 out-of-scope or unsafe questions) | Must |
| E5 | Results table in README, regenerated by a script | Must |
| E6 | Evaluation runs per language and applies the stable/experimental gate from section 4.3 | Must |

---

## 6. Non-functional Requirements

| Area | Requirement |
|------|-------------|
| Performance | p95 response under 8 seconds; retrieval under 1 second |
| Reliability | Graceful error message if the LLM or vector store is unavailable |
| Safety | No dosage advice, no diagnosis, emergency escalation, disclaimer on all answers |
| Privacy | No accounts, no personal data stored; log only anonymized question text and feedback; no IP storage |
| Security | API keys in environment variables only; rate limiting on the API; input length limit |
| Accessibility | Mobile-first layout, readable font sizes, Odia and Devanagari font support |
| Maintainability | Type hints, linting, tests, CI on every push |
| Cost | Run within free tiers where possible; document estimated cost per 1,000 queries |

---

## 7. System Architecture

### 7.1 High-level flow

```
User question
   |
   v
[React UI] --> [FastAPI backend]
                  |
                  +--> Language detection
                  +--> Safety pre-check (emergency, dosage, out-of-scope)
                  +--> Embed question (multilingual model)
                  +--> Vector search (top-k) --> confidence check
                  +--> Prompt builder (passages + rules + target language)
                  +--> LLM generation
                  +--> Post-check (citations present, language matches)
                  |
                  v
          Answer + citations + disclaimer
```

### 7.2 Components

| Component | Responsibility | Suggested tech |
|-----------|----------------|----------------|
| Frontend | Chat UI, language switcher, citations, feedback | React, Vite, Tailwind |
| API | Endpoints, validation, rate limiting | FastAPI, Pydantic |
| Ingestion pipeline | Download, clean, chunk, embed | Python, PyMuPDF, BeautifulSoup |
| Embedding model | Cross-lingual vectors | multilingual-e5 or BGE-M3 (open source) |
| Vector store | Similarity search | Chroma or FAISS |
| LLM | Grounded answer generation | An LLM API or an open model; keep behind an interface so it can be swapped |
| Evaluation | Metrics and reports | Python scripts, pytest |
| Storage | Feedback and anonymized logs | SQLite (local) or MySQL |
| Deployment | Hosting | Backend on Render or Hugging Face Spaces; frontend on Vercel |
| Language registry | Per-language settings, keywords, disclaimers, status | `config/languages.yaml` read by API, safety layer, UI, and evaluation |

### 7.3 Key design decisions to document in the README

1. **Cross-lingual retrieval vs translate-then-retrieve.** Compare both on the test set and record which wins.
2. **Chunk size and overlap.** Try 2 or 3 settings and report the effect on Recall@5.
3. **Confidence threshold for refusal.** Tune it on a validation split and show the trade-off between answered and refused questions.
4. **Answer language control.** Prompt rules plus a post-check that the output language matches the question.
5. **Per-language model choice.** Test two or three LLMs and the embedding model on each language, and record which one is used per language. Re-run the translate-then-retrieve vs cross-lingual comparison whenever a language is added.

### 7.4 Prompt rules (generation)

- Use only the provided passages.
- If the passages do not contain the answer, say so.
- Answer in the user's language, in simple words suitable for a general reader.
- Never state doses, brand names for treatment, or diagnoses.
- Cite the passage numbers used.

---

## 8. Data Plan

### 8.1 Candidate sources (verify license and terms before use)

- World Health Organization fact sheets (several are available in Hindi).
- Ministry of Health and Family Welfare, India: public guidelines and immunization material.
- National Health Mission and state health department pages (Odisha) for Odia content.
- National Vector Borne Disease Control Programme material.
- ICMR and ICMR-NIN dietary guidance.

Record each source in `SOURCES.md` with URL, language, date accessed, and usage terms. Do not include any source whose terms forbid reuse. Do not use real patient data.

### 8.2 Processing steps

1. Collect files into `data/raw/`.
2. Extract text; remove headers, footers, navigation text.
3. Split into chunks of about 200 to 400 tokens with overlap.
4. Attach metadata: source ID, title, language, topic, URL, page or section.
5. Embed and store.
6. Write ingestion statistics (documents, chunks per language) to a report.

### 8.3 Evaluation dataset

- 150 or more questions: 50 each in English, Hindi, Odia, spread across the 8 topics. Each added language needs about 60 more (50 questions plus 10 refusal cases) before it can be marked stable.
- For each question: gold source passage ID, reference answer summary, and whether it should be answered or refused.
- Add at least 30 refusal cases (out-of-scope, dosage, diagnosis, emergency).
- Have a native speaker review the Odia and Hindi questions if possible, and note this in the README.
- Keep a separate validation split (for tuning) and test split (reported once).

---

## 9. API Specification

### POST /api/ask

Request:
```json
{
  "question": "string",
  "language": "auto | en | hi | or",
  "session_id": "string (optional)"
}
```

Response:
```json
{
  "answer": "string",
  "language": "hi",
  "status": "answered | refused | emergency",
  "citations": [
    {"id": 1, "title": "string", "url": "string", "section": "string"}
  ],
  "disclaimer": "string",
  "request_id": "string"
}
```

### POST /api/feedback

```json
{"request_id": "string", "rating": "up | down", "comment": "string (optional)"}
```

### GET /api/health

Returns service status and knowledge base version.

---

## 10. UI Requirements

- Single chat screen: input box, language selector, message list.
- Each answer shows citation chips that link to the source.
- Persistent disclaimer line under the input.
- Emergency state shown in a distinct style with clear next steps.
- Example question buttons per language for first-time users.
- Works at 360 px width; loads fonts for Devanagari and Odia scripts.

---

## 11. Evaluation and Success Metrics

| Metric | Definition | Target (v1) |
|--------|------------|-------------|
| Recall@5 | Gold passage appears in top 5 | 85% or higher overall; Odia no more than 10 points below English |
| MRR | Mean reciprocal rank of gold passage | 0.70 or higher |
| Faithfulness | Share of answer claims supported by retrieved text | 90% or higher |
| Citation correctness | Cited passage actually supports the claim | 90% or higher |
| Refusal accuracy | Correct refusal on out-of-scope or unsafe set | 90% or higher |
| False refusal rate | Answerable questions wrongly refused | 15% or lower |
| Language match | Answer language equals question language | 98% or higher |
| Latency p95 | End-to-end | Under 8 seconds |
| Per-language gate | A language is `stable` only if it meets the language targets above and the section 4.3 checklist | Applies to every language |

Report results per language and per topic. Include a failure analysis section with at least 10 real failure cases and a note on the cause of each.

---

## 12. Safety and Ethics

- Informational only; disclaimer on every answer and in the README.
- Emergency keyword list in all three languages, reviewed by a native speaker.
- No dosage, diagnosis, or treatment recommendations.
- No collection of personal health data; anonymized logs only.
- Transparent about weaker Odia performance if the numbers show it.
- Document dataset coverage gaps and bias (rural vs urban phrasing, dialect differences).
- Add a "Known limitations" section to the README.

---

## 13. Testing Plan (pass/fail)

| Test | Pass condition |
|------|----------------|
| Ingestion runs end to end | Command completes; chunk count greater than 0 for every language |
| Retrieval smoke test | 10 sample questions each return the expected source in top 5 |
| API contract | `/api/ask` returns the response schema for valid input; 422 for invalid input |
| Emergency detection | All emergency test phrases return status `emergency` |
| Dosage refusal | All dosage test phrases return status `refused` |
| Out-of-scope refusal | All 30 refusal cases refused at the target rate |
| Language match | Output language matches input on the 150 question set at target rate |
| Frontend | Question can be sent, answer and citations render, feedback posts |
| CI | Lint, unit tests, and smoke evaluation pass on every push |

---

## 14. Milestones and Timeline (v1 in about 6 weeks, part-time; v1.1 and v2 follow)

| Week | Deliverable |
|------|-------------|
| 1 | Repo setup, source list, ingestion pipeline, first chunks and embeddings |
| 2 | Retrieval working with baseline evaluation; test set drafted |
| 3 | Generation, citations, refusal and safety layer; API complete |
| 4 | React UI, feedback, deployment |
| 5 | Full evaluation, tuning, failure analysis |
| 6 | README, demo GIF, polish, release v1.0 |
| 7 to 9 | v1.1: refactor to the language registry, onboard Bengali, Telugu, Tamil using the checklist, release v1.1.0 |
| 10 to 14 | v2: onboard Marathi, Gujarati, Kannada, Malayalam, Punjabi in batches, cross-language results table, release v2.0.0 |

---

## 15. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Few Odia source documents | Weak Odia coverage | Use cross-lingual retrieval from English sources; report Odia numbers honestly; add Odia sources gradually |
| LLM writes poor Odia | Low answer quality | Test multiple models; allow showing source passage text; report per-language scores |
| Hallucination | Unsafe answers | Strict grounding prompt, faithfulness checks, refusal threshold |
| Source licensing | Legal issues | Maintain `SOURCES.md`; use only permitted sources; link instead of copying where unclear |
| Scope creep | Unfinished project | Fix 8 topics and 3 languages for v1; park other ideas in the roadmap |
| Hosting cost | Project goes offline | Use free tiers, cache frequent answers, add rate limits |
| Evaluation effort grows with each language | Delays or untested languages | Fixed checklist, about 60 labeled questions per language, add languages in small batches of 2 or 3 |
| No native-speaker reviewer for a language | Unsafe or wrong emergency keywords and disclaimers | Do not mark the language stable; keep it experimental until reviewed |
| Quality drops silently in less-tested languages | Misleading users | Publish per-language results; show the experimental label in the UI |

---

## 16. Roadmap (after v1)

- Voice input and output.
- Additional languages beyond the v2 set (see section 4.3).
- WhatsApp or SMS interface for low-connectivity users.
- Offline-friendly lightweight mode.
- Feedback-driven knowledge base improvements.

---

## 17. Repository Structure

```
health-faq-assistant/
  README.md
  PRD.md
  SOURCES.md
  LICENSE
  .gitignore
  .env.example
  config/
    languages.yaml
  docker-compose.yml
  Dockerfile
  requirements.txt
  .github/
    workflows/ci.yml
    ISSUE_TEMPLATE/
  data/
    raw/            (not committed if large; document download script)
    processed/
    eval/           (questions.csv, refusals.csv)
  src/
    ingestion/
    retrieval/
    generation/
    safety/
    api/
    evaluation/
  tests/
  frontend/
  docs/
    architecture.png
    evaluation-report.md
    demo.gif
```

---

## 18. GitHub Rollout: Part by Part

Goal: the repository history should look like a real project built in stages. Each part is a branch, merged by pull request, with a tag. Commit small and often with clear messages.

### Part 0: Repository setup

Branch: `main`
Add:
- Repo named `health-faq-assistant` with a one-line description and topics (`rag`, `nlp`, `multilingual`, `healthcare`, `fastapi`, `react`).
- `README.md` skeleton (title, problem, planned features, status "in progress").
- `PRD.md` (this document).
- `.gitignore`, `LICENSE` (MIT), `.env.example`.
- `SOURCES.md` with the initial source list.

Commit messages:
- `docs: add PRD and project README skeleton`
- `chore: add gitignore, license, env example`

Pass check: repo opens with a clear README and the PRD visible.
Tag: none.

### Part 1: Data ingestion pipeline

Branch: `feature/ingestion`
Add:
- Scripts to download or load documents listed in `SOURCES.md`.
- Text extraction, cleaning, chunking with metadata.
- Ingestion statistics report.
- Unit tests for chunking and cleaning.

Commit messages:
- `feat(ingestion): add PDF and HTML text extraction`
- `feat(ingestion): add chunking with metadata`
- `test(ingestion): add chunking tests`

Pass check: `python -m src.ingestion.run` completes and prints chunks per language.
Tag: `v0.1.0`.

### Part 2: Embeddings and retrieval

Branch: `feature/retrieval`
Add:
- Embedding and vector store module.
- Search function with top-k and confidence score.
- First draft of the evaluation questions (30 questions to start).
- Retrieval evaluation script producing Recall@5 and MRR.

Commit messages:
- `feat(retrieval): add multilingual embeddings and vector store`
- `feat(eval): add retrieval metrics script`
- `docs: record baseline retrieval results`

Pass check: evaluation script prints metrics; baseline numbers added to README.
Tag: `v0.2.0`.

### Part 3: Generation with citations

Branch: `feature/generation`
Add:
- LLM interface (swappable provider).
- Prompt template with grounding rules and language control.
- Citation formatting and post-checks.

Commit messages:
- `feat(generation): add grounded answer generation`
- `feat(generation): add citation extraction and language check`
- `test(generation): add citation and language tests`

Pass check: 10 sample questions return answers with valid citations.
Tag: `v0.3.0`.

### Part 4: Safety layer

Branch: `feature/safety`
Add:
- Emergency detection (three languages).
- Dosage and diagnosis refusal rules.
- Out-of-scope and low-confidence refusal.
- Refusal test set (30 or more cases).

Commit messages:
- `feat(safety): add emergency and dosage detection`
- `feat(safety): add low-confidence refusal`
- `test(safety): add refusal test suite`

Pass check: all emergency and dosage tests pass.
Tag: `v0.4.0`.

### Part 5: API

Branch: `feature/api`
Add:
- FastAPI app with `/api/ask`, `/api/feedback`, `/api/health`.
- Validation, rate limiting, error handling.
- API tests and OpenAPI docs.
- Dockerfile.

Commit messages:
- `feat(api): add ask endpoint`
- `feat(api): add feedback and health endpoints`
- `test(api): add contract tests`
- `chore: add Dockerfile`

Pass check: tests pass; `docker run` serves the API.
Tag: `v0.5.0`.

### Part 6: Frontend

Branch: `feature/frontend`
Add:
- React chat UI, language switcher, citation chips, feedback buttons, disclaimer.
- Mobile layout and font support for Devanagari and Odia.

Commit messages:
- `feat(frontend): add chat interface`
- `feat(frontend): add language switcher and citations`
- `style(frontend): mobile layout and script fonts`

Pass check: full question-to-answer flow works locally on desktop and phone width.
Tag: `v0.6.0`.

### Part 7: CI and deployment

Branch: `feature/deploy`
Add:
- GitHub Actions workflow: lint, tests, smoke evaluation.
- Deployment config and live URLs.
- Live demo link and status badge in README.

Commit messages:
- `ci: add lint, test, and smoke evaluation workflow`
- `chore: add deployment configuration`
- `docs: add live demo link`

Pass check: CI is green; the live link answers a question.
Tag: `v0.7.0`.

### Part 8: Full evaluation and tuning

Branch: `feature/evaluation`
Add:
- Complete 150-question test set and refusal set.
- Per-language, per-topic results.
- Experiments table (chunk size, translate-then-retrieve vs cross-lingual, threshold).
- `docs/evaluation-report.md` with failure analysis.

Commit messages:
- `feat(eval): complete evaluation dataset`
- `docs: add evaluation report and failure analysis`
- `perf(retrieval): tune chunk size and threshold`

Pass check: metrics table in README is generated by a script and matches the report.
Tag: `v0.8.0`.

### Part 9: Final README and release

Branch: `docs/final`
Add:
- Final README: demo GIF, architecture diagram, results table, quick start, limitations, roadmap.
- `CONTRIBUTING.md` and issue templates.
- Short write-up (blog post or LinkedIn post) linking to the repo.

Commit messages:
- `docs: final README with results and demo`
- `docs: add limitations and roadmap`

Pass check: a new reader can run the project from the README in under 10 minutes.
Tag and release: `v1.0.0` with release notes.

### Part 10: Language registry refactor (v1.1 groundwork)

Branch: `feature/language-registry`
Add:
- `config/languages.yaml` with entries for English, Hindi, Odia.
- Code changes so the API, safety layer, UI, and evaluation read languages from the registry.
- Per-language evaluation output and the `experimental` label in the UI.
- Tests that fail if a language entry is missing required fields.

Commit messages:
- `refactor: load languages from registry`
- `feat(ui): show experimental label by status`
- `feat(eval): report metrics per language`
- `test: validate registry entries`

Pass check: removing a field from a registry entry makes the validation test fail; existing v1 results are unchanged.
Tag: `v1.0.1`.

### Part 11: Onboard new languages (repeat per language or batch)

Branch: `feature/lang-<code>` (for example `feature/lang-bn`)
Add, for each language:
- Sources added to `SOURCES.md` and `data/raw/`.
- Registry entry with keywords, disclaimer, UI strings, and font.
- `data/eval/<code>.csv` with 50 questions and 10 refusal cases.
- Results added to the README per-language table and `docs/evaluation-report.md`.

Commit messages:
- `data(<code>): add sources and ingest`
- `feat(<code>): add registry entry and UI strings`
- `eval(<code>): add test set and results`
- `docs(<code>): update language table and status`

Pass check: the section 4.3 checklist passes, or the language is committed as `experimental` with its numbers published.
Tags: `v1.1.0` after the first batch (Bengali, Telugu, Tamil), `v2.0.0` after the second batch.

### Git habits that reviewers notice

- One branch per part, merged through a pull request with a short description.
- Conventional commit messages (`feat`, `fix`, `docs`, `test`, `chore`).
- Open GitHub Issues for planned work and close them from commits.
- A Projects board with columns: Backlog, In progress, Done.
- No secrets in the history; use `.env` and keep `.env.example` in the repo.
- Commit regularly across weeks rather than in one large upload.

---

## 19. README Outline (final)

1. Title, one-line description, badges, live demo link
2. Demo GIF
3. Problem and motivation
4. Features
5. Architecture diagram
6. Results table (per language) and key findings
7. Quick start (local and Docker)
8. Project structure
9. Data sources and licensing
10. Safety design and limitations
11. Evaluation method
12. Roadmap
13. License and disclaimer

---

## 20. Interview Talking Points

- Why cross-lingual retrieval, and what the experiment showed.
- How the refusal threshold was chosen and its trade-offs.
- Where Odia performance lagged and what you did about it.
- A failure case you found and how you fixed it.
- How you would add voice and more languages.

---

## 21. Open Questions

- Which LLM and embedding model give the best Odia results within budget?
- Is a native-speaker review available for the evaluation questions?
- Which Odia-language official sources can be used under their terms?
- Which languages come first in v1.1? The default plan is Bengali, Telugu, Tamil.
- Are native-speaker reviewers available for each added language, or will some stay experimental?
