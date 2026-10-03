# Project Announcement / LinkedIn Post

**Title**: Bridging the Local Language Health Gap: Building a Safety-First Multilingual RAG Assistant for Indian Communities 🇮🇳

Most authoritative medical knowledge is published exclusively in English. For millions across India, accessing accurate guidance in **Hindi, Odia**, or regional languages often means navigating misinformation, informal WhatsApp forwards, or hallucinated AI chat responses that provide unsafe medical claims without sources.

To address this challenge, I built the **Multilingual Health FAQ Assistant**: an open-source, source-grounded Retrieval-Augmented Generation (RAG) assistant designed specifically for community health awareness.

### 💡 Key Engineering Highlights:
1. **🌐 Cross-Lingual Semantic Retrieval**: Users can ask complex health questions in Hindi or Odia and retrieve verified passages even if the original public health document was published in English or official state circulars.
2. **🛡️ Multi-Tier Medical Safety Guardrails**:
   - **Emergency Detection**: Instant native-script detection for life-threatening emergencies (chest pain, stroke, unconsciousness) triggering a direct escalation to call 112/108.
   - **Refusal System**: 100% refusal rate on requests for drug dosages, prescriptions, and clinical diagnoses.
   - **Confidence Filtering**: Calibrated threshold rejecting out-of-scope non-medical queries.
3. **📚 Transparent Attribution**: 100% of answers provide clickable citations directly linking to official WHO, MoHFW, and State Health Mission documents.
4. **📊 Measured Benchmark Results (150 Questions + 31 Refusal Cases)**:
   - **Recall@5**: 93.3% overall (English: 94.0%, Hindi: 94.0%, Odia: 92.0% — well within the 10-point gate).
   - **Mean Reciprocal Rank (MRR)**: 0.876
   - **Answer Faithfulness**: 92.7%
   - **Refusal Accuracy**: 100.0%
   - **End-to-end Latency (p95)**: ~100ms
5. **⚙️ Extensible Language Registry**: Adding new languages (Bengali, Telugu, Tamil) requires zero code changes — just updating a declarative configuration file (`config/languages.yaml`) and passing automated quality gates.

Check out the full repository, evaluation report, and architecture:  
👉 GitHub: https://github.com/Asifkarim683/Multilingual-health-FAQ-assistant-for-local-languages

Feedback and contributions are warmly welcome!

#AI #HealthcareAI #RAG #NLP #Multilingual #FastAPI #React #Python #OpenSource #IndicNLP
