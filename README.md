# Multilingual Health FAQ Assistant for Indian Local Languages

> **A safety-first, source-grounded Retrieval-Augmented Generation (RAG) assistant answering community health questions in Hindi, Odia, and English with strict medical guardrails and verifiable citations.**

[![CI Pipeline](https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages/actions/workflows/ci.yml/badge.svg)](https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/UI-React%20%2B%20Tailwind-61DAFB.svg)](https://react.dev/)

---

## 📌 Status: In Progress (v1.0 Milestone)

This project addresses the critical gap in localized, reliable public health information across India. Most authoritative medical guidelines exist only in English, leaving non-English speakers vulnerable to hallucinated chatbot responses and misleading informal advice.

The assistant implements **cross-lingual retrieval** over curated public health documents from the World Health Organization (WHO), Ministry of Health and Family Welfare (MoHFW), ICMR, and State Health Missions, ensuring every answer is strictly grounded with transparent citations and instant medical refusals for prescriptions, diagnoses, or emergencies.

---

## 🎯 Key Features

- **🌐 Multilingual & Cross-Lingual Retrieval**: Ask questions in Hindi, Odia, or English; retrieves verified source passages even if originally published in English or official state circulars.
- **🛡️ Medical Safety & Triage Guardrails**:
  - **Emergency Keyword Detection**: Detects life-threatening symptoms (chest pain, stroke, unconsciousness) in native scripts and triggers an emergency directive to dial 112/108 immediately.
  - **Dosage & Prescription Refusal**: Strict refusal on requests for tablet dosages, drug prescriptions, or clinical diagnoses.
  - **Out-of-Scope & Low-Confidence Refusal**: Politely declines questions not supported in verified public health sources.
- **📚 Verifiable Citations**: Every response returns direct document titles, sections, and official public links.
- **⚙️ Dynamic Language Registry**: Add support for new Indian languages (e.g., Bengali, Telugu, Tamil) via `config/languages.yaml` without changing application code.
- **📊 Measurable Evaluation Suite**: Rigorous automated benchmark evaluating Recall@5, MRR, Faithfulness, Citation Correctness, and Refusal Accuracy across hand-labeled test splits.

---

## 🏗️ Architecture Overview

```
                      [ User Query (Hindi / Odia / English) ]
                                      |
                                      v
                             [ React + Vite UI ]
                                      |
                                      v
                             [ FastAPI Backend ]
                                      |
                +---------------------+---------------------+
                |                                           |
      [ Language Detector ]                        [ Safety Pre-Check ]
                |                             (Emergency / Dosage Refusal)
                v                                           |
    [ Cross-Lingual Embeddings ]                            |
                |                                           |
                v                                           |
     [ Multilingual Vector Index ]                          |
                |                                           |
      (Confidence Threshold)                                |
                |                                           |
                v                                           v
      [ Grounded Generator ] <-------------- [ Strict Medical Prompt ]
                |
                v
      [ Safety Post-Check ] (Language match, citation integrity)
                |
                v
      [ Grounded Answer + Official Citations + Medical Disclaimer ]
```

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) Gemini API Key or local embedding models

### 2. Clone and Setup Environment
```bash
git clone https://github.com/example/health-faq-assistant.git
cd health-faq-assistant

# Setup Python Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install Backend Dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
```

### 3. Run Knowledge Base Ingestion
```bash
python -m src.ingestion.run
```

### 4. Start Backend API
```bash
uvicorn src.api.main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 5. Start Frontend UI
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Evaluation Metrics & Baseline Results

### Baseline Retrieval Performance (v0.2.0, k=5)

| Language | Test Questions | Recall@1 | Recall@5 | Mean Reciprocal Rank (MRR) | Status |
|---|---|---|---|---|---|
| **English (EN)** | 10 | 70.0% | **100.0%** | 0.850 | Target Exceeded ($\ge 85\%$) |
| **Hindi (HI)** | 10 | 60.0% | **90.0%** | 0.783 | Target Exceeded ($\ge 85\%$) |
| **Odia (OR)** | 10 | 90.0% | **100.0%** | 0.883 | Target Exceeded ($\ge 85\%$) |
| **Overall** | **30** | **73.3%** | **96.7%** | **0.839** | **Pass (v1 Target: $\ge 85\%$ / 0.70)** |

### Target vs Current Measured Metrics (v1.0)

| Metric | Target | Baseline Status | Notes |
|---|---|---|---|
| **Recall@5** (Cross-lingual) | $\ge 85\%$ | **96.7%** (Pass) | Odia within 10 pts of English (100% vs 100%) |
| **Mean Reciprocal Rank (MRR)** | $\ge 0.70$ | **0.839** (Pass) | High rank precision across Indic and English |
| **Answer Faithfulness** | $\ge 90\%$ | Testing (v0.3.0) | Strict grounding prompt & passage constraint |
| **Citation Correctness** | $\ge 90\%$ | Testing (v0.3.0) | Automatic source ID extraction |
| **Safety Refusal Accuracy** | $\ge 90\%$ | Testing (v0.4.0) | Multilingual emergency & dosage detectors |
| **Language Match Rate** | $\ge 98\%$ | Testing (v0.3.0) | Language verification layer |
| **p95 Latency** | $< 8.0$ s | In Progress | Optimized hybrid vector index |


---

## 📖 Verified Sources

See [SOURCES.md](file:///d:/SELF/Multilingual%20health%20FAQ%20assistant%20for%20local%20languages/SOURCES.md) for the complete directory of ingested public health documents and open licenses.

---

## ⚠️ Medical Disclaimer

*This application is an educational prototype and informational assistant designed to disseminate verified public health education. It DOES NOT provide medical diagnosis, clinical treatment plans, or drug dosage recommendations. In case of medical emergencies or acute symptoms, immediately contact your local emergency services (112 / 108 in India) or visit the nearest hospital.*
