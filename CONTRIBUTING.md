# Contributing to Multilingual Health FAQ Assistant

Thank you for your interest in contributing to the **Multilingual Health FAQ Assistant**!

This project provides verified, source-grounded health information to non-English speaking communities in India (currently Hindi, Odia, English, with planned expansion to Bengali, Telugu, and Tamil).

---

## 🧭 Code of Conduct & Medical Safety Principles

Because this assistant operates in the high-stakes public health domain:
1. **Never weaken safety guardrails**: Pull requests that bypass emergency keyword detection, dosage refusal, or source citation requirements will be rejected.
2. **Grounding is absolute**: Any newly proposed retrieval or generation pipeline must guarantee that generated claims are fully supported by verifiable public health documents.
3. **No proprietary or clinical data**: Do not commit patient health records, unverified home remedies, or copyrighted text without permission.

---

## 🛠️ Development Setup

1. **Fork and clone** the repository.
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **Run tests**:
   ```bash
   pytest tests/
   ```
4. **Run evaluation suite**:
   ```bash
   python -m src.evaluation.evaluate_all
   ```

---

## 🌐 Onboarding a New Language

To add a new Indian language (e.g. Marathi, Gujarati, Kannada):
1. **Verify Official Sources**: Find at least 3 official public health documents (WHO, MoHFW, State Health Mission) covering the 8 core topics. Record them in `SOURCES.md`.
2. **Add Language Registry Entry**: In `config/languages.yaml`, add the language code, native name, script, font, emergency keywords, disclaimer, and example questions.
3. **Add Evaluation Questions**: Create `data/eval/<code>.csv` with 50 questions and 10 refusal cases with gold passage references.
4. **Run Quality Gates**: Run `python -m src.evaluation.evaluate_all`. The language must satisfy:
   - Recall@5 within 10 percentage points of English
   - Faithfulness $\ge 90\%$
   - Refusal accuracy $\ge 90\%$
   - Native-speaker review of emergency keywords.

---

## 🌿 Git & Pull Request Guidelines

- Branch naming: `feature/<name>`, `fix/<name>`, `docs/<name>`.
- Write clear conventional commit messages (`feat: ...`, `fix: ...`, `test: ...`, `docs: ...`).
- Ensure all tests pass before submitting a PR.
