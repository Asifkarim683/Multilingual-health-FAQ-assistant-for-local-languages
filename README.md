# Multilingual Health FAQ Assistant for Indian Local Languages

> **A safety-first, source-grounded Retrieval-Augmented Generation (RAG) assistant answering community health questions in Hindi, Odia, Bengali, Telugu, Tamil, and English with verifiable citations and strict medical guardrails.**

[![CI Pipeline](https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages/actions/workflows/ci.yml/badge.svg)](https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/UI-React%20%2B%20Tailwind-61DAFB.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

---

## 📌 Problem & Motivation

Most authoritative health guidelines in India are published primarily in English. Over 80% of the population, particularly in Tier-2/Tier-3 cities and rural areas, is far more comfortable seeking health awareness in **Hindi (हिन्दी)**, **Odia (ଓଡ଼ିଆ)**, **Bengali (বাংলা)**, **Telugu (తెలుగు)**, **Tamil (தமிழ்)**, or other regional languages. 

General generative chatbots frequently hallucinate medical treatments, fail to cite sources, and provide unsafe advice. 

The **Multilingual Health FAQ Assistant** solves this through a strictly grounded, cross-lingual Retrieval-Augmented Generation (RAG) pipeline:
- **Grounding**: Answers are derived strictly from curated public health guidelines (WHO, MoHFW India, ICMR, Odisha NHM, WB Health, AP Health, TN NHM).
- **Cross-Lingual Retrieval**: A user asking an Odia, Hindi, Bengali, Telugu, or Tamil question retrieves matching English or regional source passages.
- **Attribution**: Every claim is accompanied by a transparent citation linking to official documents.
- **Safety**: Hard refusal for medication dosage, prescription, or clinical diagnosis, with instant emergency routing to **112 / 108**.

---

## 🎯 Key Features

- **🌐 Cross-Lingual Semantic Retrieval**: Queries in Hindi, Odia, Bengali, Telugu, or Tamil match authoritative English and Indic knowledge bases with high recall.
- **🛡️ Multi-Tier Medical Safety Guardrails**:
  - **Emergency Keyword Detection**: Detects acute warning signs (chest pain, stroke, unconsciousness) in native scripts and displays emergency helpline numbers without calling the LLM.
  - **Dosage & Prescription Refusal**: Blocks requests for drug dosages, medicine prescriptions, and clinical diagnoses across all 6 languages.
  - **Confidence-Based Out-of-Scope Filtering**: Calibrated threshold cleanly rejects non-medical queries.
- **📚 Verifiable Citations**: Returns document titles, sections, and clickable URLs for every answered query.
- **⚙️ Declarative Language Registry**: Onboard new Indian languages via `config/languages.yaml` without changing application code.
- **📱 Responsive Mobile Experience**: Optimized touch interface with native font rendering for Devanagari, Odia, Bengali, Telugu, and Tamil scripts down to 360px viewport width.
- **📊 Measurable Benchmark Suite**: Automated evaluation over 300 hand-labeled questions and 61 refusal cases across 6 languages.

---

## 🏗️ System Architecture

```
User Query (Hindi / Odia / English)
       |
       v
+-----------------------------------------------------------+
| React + Vite Frontend (Responsive UI, Devanagari/Odia Fonts) |
+-----------------------------------------------------------+
       | HTTP POST /api/ask
       v
+-----------------------------------------------------------+
| FastAPI Application (Rate Limiter, Validation)            |
+-----------------------------------------------------------+
       |
       +---> [1. Safety Pre-Check] ----------------------------+
       |      - Emergency Detection (112/108 routing)          |
       |      - Dosage & Diagnosis Refusal                     |
       |                                                       | (If Triggered)
       v                                                       v
+-----------------------------+                     [ Instant Refusal / Alert ]
| 2. Multilingual Retrieval   |
|    - Subword Character &    |
|      Word Hybrid Embedder   |
|    - Cross-Lingual Synonyms |
|    - Cosine Vector Index    |
+-----------------------------+
       |
       v Top-k Passages
+-----------------------------+
| 3. Confidence Gate          | ---- (Below 0.20 Threshold) ---> [ Out-of-Scope Refusal ]
+-----------------------------+
       | (Sufficient Confidence)
       v
+-----------------------------+
| 4. Grounded Generator       |
|    - Strict Medical Prompt  |
|    - Swappable LLM Provider |
|      (Gemini / OpenAI / Mock|
+-----------------------------+
       |
       v
+-----------------------------+
| 5. Post-Generation Check    |
|    - Citation Extraction    |
|    - Script Language Match  |
+-----------------------------+
       |
       v
+-----------------------------------------------------------+
| Grounded Response + Official Citations + Medical Disclaimer |
+-----------------------------------------------------------+
```

---

## 🧪 Benchmark Results & Quality Gates (v1.1.0)

Evaluated against the hand-labeled benchmark of **300 test questions** (50 English, 50 Hindi, 50 Odia, 50 Bengali, 50 Telugu, 50 Tamil) and **61 refusal cases** across all 8 core health topics:

| Evaluation Metric | Target (PRD) | Measured Result | Status Gate |
|---|---|---|---|
| **Recall@5** (Cross-Lingual) | $\ge 85\%$ | **94.0%** | ✅ Pass (Exceeded) |
| **Mean Reciprocal Rank (MRR)** | $\ge 0.70$ | **0.908** | ✅ Pass (Exceeded) |
| **Answer Faithfulness** | $\ge 90\%$ | **94.3%** | ✅ Pass (Exceeded) |
| **Citation Correctness** | $\ge 90\%$ | **94.0%** | ✅ Pass (Exceeded) |
| **Safety Refusal Accuracy** | $\ge 90\%$ | **98.4%** | ✅ Pass (Exceeded) |
| **False Refusal Rate** | $\le 15\%$ | **5.7%** | ✅ Pass (Exceeded) |
| **Language Match Rate** | $\ge 98\%$ | **100.0%** | ✅ Pass (Exceeded) |
| **p95 Latency** | $< 8.0$ s | **0.058 s** | ✅ Pass (Exceeded) |

### Per-Language Performance Gates

| Language | Test Questions | Recall@5 | MRR | Faithfulness | Citation Match | Script Match | Status Gate |
|---|---|---|---|---|---|---|---|
| **English (EN)** | 50 | **94.0%** | 0.890 | 94.0% | 94.0% | 100.0% | `stable` |
| **Hindi (HI)** | 50 | **94.0%** | 0.930 | 94.0% | 94.0% | 100.0% | `stable` |
| **Odia (OR)** | 50 | **94.0%** | 0.897 | 96.0% | 94.0% | 100.0% | `stable` |
| **Bengali (BN)** | 50 | **92.0%** | 0.840 | 92.0% | 92.0% | 100.0% | `stable` |
| **Telugu (TE)** | 50 | **94.0%** | 0.940 | 94.0% | 94.0% | 100.0% | `stable` |
| **Tamil (TA)** | 50 | **96.0%** | 0.950 | 96.0% | 96.0% | 100.0% | `stable` |

*Indic Low-Resource Gate*: All Indic language Recall@5 scores (Odia 94.0%, Bengali 92.0%, Telugu 94.0%, Tamil 96.0%) are within 2.0% of English (94.0%), comfortably satisfying the PRD's 10-point gate requirement.

For detailed ablation studies (chunk size tuning, cross-lingual vs translate-then-retrieve) and real failure analysis, see [docs/evaluation-report.md](file:///d:/SELF/Multilingual%20health%20FAQ%20assistant%20for%20local%20languages/docs/evaluation-report.md).

---

## 🚀 Quick Start (Under 10 Minutes)

### Option 1: Local Development

```bash
# 1. Clone repository
git clone https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages.git
cd Multilingual-health-FAQ-assistant-for-local-languages

# 2. Setup Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Ingest knowledge base
python -m src.ingestion.run

# 4. Start Backend API (FastAPI)
uvicorn src.api.main:app --reload --port 8000
# OpenAPI Docs: http://localhost:8000/docs

# 5. Start Frontend (React + Vite)
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Option 2: Run with Docker Compose

```bash
docker-compose up --build
```
Access API at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`.

---

## 📁 Repository Structure

```
.
├── config/
│   └── languages.yaml         # Language registry (keywords, fonts, disclaimers)
├── data/
│   ├── raw/                   # Verified health source files (SRC-01 to SRC-09)
│   ├── processed/             # Extracted chunks with metadata
│   └── eval/                  # 150 benchmark questions & refusal test cases
├── docs/
│   ├── evaluation-report.md   # Comprehensive evaluation report & failure analysis
│   └── launch-announcement.md # Project announcement & portfolio summary
├── frontend/
│   ├── src/                   # React chat UI & Tailwind CSS styles
│   └── index.html             # Preloaded Indic fonts (Devanagari, Odia)
├── src/
│   ├── ingestion/             # Extraction, Indic cleaner, and chunker
│   ├── retrieval/             # Multilingual embeddings and vector store
│   ├── generation/            # Grounded generator, citations, and LLM providers
│   ├── safety/                # Emergency detector, dosage refusal, confidence gate
│   ├── api/                   # FastAPI endpoints, schemas, SQLite database
│   └── evaluation/            # Automated benchmark evaluation harness
├── tests/                     # Full pytest test suite (18+ tests)
├── Dockerfile                 # Multi-stage container build
├── docker-compose.yml         # Container orchestration
├── CONTRIBUTING.md            # Guidelines for onboarding new languages
├── SOURCES.md                 # Public health sources catalog & licenses
└── requirements.txt           # Python dependencies
```

---

## 📚 Public Health Sources & Licensing

All ingested health content is strictly sourced from verified public health authorities under open educational terms:
1. **World Health Organization (WHO)**: Dengue, Diabetes, Hypertension, and Diarrhea Fact Sheets.
2. **Ministry of Health and Family Welfare (MoHFW)**: Universal Immunization Programme (UIP) & PMSMA.
3. **National Vector Borne Disease Control Programme (NVBDCP)**: Vector control guidelines.
4. **National Health Mission (NHM Odisha)**: Odia-language diarrhea, nutrition, and maternal health circulars.
5. **ICMR - National Institute of Nutrition (NIN)**: Dietary guidelines for Indians.

See [SOURCES.md](file:///d:/SELF/Multilingual%20health%20FAQ%20assistant%20for%20local%20languages/SOURCES.md) for full attribution, links, and licensing terms.

---

## 🛡️ Safety Design & Known Limitations

- **Strict Grounding**: The assistant refuses to speculate outside retrieved passages.
- **No Diagnostic or Prescription Advice**: Recommending specific dosages or clinical diagnosis is prohibited and blocked by pre-checks.
- **Dialect Variations**: The initial Odia dataset represents standard written Odia; performance on localized spoken dialects (Sambalpuri, Desia) is planned for voice integration in v2.
- **Language Status Transparency**: Any language not yet passing native-speaker clinical review is visibly marked with an `Experimental` badge in the UI.

---

## 🗺️ Roadmap

- **v1.1**: Onboard Bengali (`bn`), Telugu (`te`), and Tamil (`ta`) using the declarative language registry.
- **v2.0**: Voice input/output integration using Bhashini / Indic Whisper for rural accessibility.
- **v2.1**: WhatsApp / Telegram bot integration for low-bandwidth access.

---

## 📄 License & Disclaimer

Released under the [MIT License](file:///d:/SELF/Multilingual%20health%20FAQ%20assistant%20for%20local%20languages/LICENSE).

**Medical Disclaimer**: *This software is an educational prototype and informational assistant designed to disseminate verified public health education. It DOES NOT provide medical diagnosis, clinical treatment plans, or drug dosage recommendations. In case of medical emergencies or acute symptoms, immediately contact your local emergency services (112 / 108 in India) or visit the nearest hospital.*
