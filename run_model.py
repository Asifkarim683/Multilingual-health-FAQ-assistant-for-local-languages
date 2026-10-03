"""Interactive CLI & Batch Runner for the Multilingual Health FAQ Assistant Model."""
import argparse
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.api.main import get_services
from src.generation.language_verifier import detect_script_language


def ask_assistant(question: str, language: str = "auto"):
    """Run a query through the full multilingual health RAG pipeline."""
    store, guardrail, generator, registry = get_services()

    # 1. Resolve Language
    if not language or language == "auto":
        resolved_lang = detect_script_language(question)
    else:
        resolved_lang = language

    lang_info = registry.get(resolved_lang, {})
    lang_name = lang_info.get("name", resolved_lang.upper())
    disclaimer = generator.get_disclaimer(resolved_lang)

    print("\n" + "=" * 70)
    print(f"QUERY:    {question}")
    print(f"LANGUAGE: {lang_name} ({resolved_lang.upper()})")
    print("-" * 70)

    # 2. Safety Pre-Check
    pre_check = guardrail.run_pre_check(question, language=resolved_lang)
    if pre_check.action in ["emergency", "refused"]:
        print(f"STATUS:   [{pre_check.action.upper()}]")
        print(f"\n{pre_check.message}\n")
        print(f"DISCLAIMER:\n{disclaimer}")
        print("=" * 70 + "\n")
        return

    # 3. Vector Retrieval
    results = store.search(question, top_k=5, lang_filter=resolved_lang)

    # 4. Confidence Filtering (Post-check)
    post_check = guardrail.run_post_retrieval_check(results, language=resolved_lang, threshold=0.20)
    if post_check.action == "refused":
        print(f"STATUS:   [OUT-OF-SCOPE REFUSED]")
        print(f"\n{post_check.message}\n")
        print(f"DISCLAIMER:\n{disclaimer}")
        print("=" * 70 + "\n")
        return

    # 5. Grounded Generation
    top_chunks = [r.to_dict() for r in results]
    gen_result = generator.generate_response(
        question=question,
        retrieved_chunks=top_chunks,
        target_language=resolved_lang,
    )

    print("STATUS:   [ANSWERED]")
    print(f"\nANSWER:\n{gen_result.answer}\n")

    if gen_result.citations:
        print("OFFICIAL CITATIONS:")
        for c in gen_result.citations:
            cid = c.get("id", 1)
            print(f"  [{cid}] {c.get('title')} - {c.get('section')}")
            print(f"      URL: {c.get('url')}")

    print(f"\nDISCLAIMER:\n{gen_result.disclaimer}")
    print("=" * 70 + "\n")


DEMO_QUESTIONS = [
    {
        "lang": "en",
        "question": "What are the common symptoms of dengue fever and warning signs?",
    },
    {
        "lang": "hi",
        "question": "डायबिटीज (मधुमेह) के शुरुआती लक्षण क्या हैं और इसे कैसे नियंत्रित करें?",
    },
    {
        "lang": "or",
        "question": "ଡେଙ୍ଗୁ ଜ୍ୱରର ମୁଖ୍ୟ ଲକ୍ଷଣ ଏବଂ ପ୍ରତିଷେଧକ ବ୍ୟବସ୍ଥା କ'ଣ?",
    },
    {
        "lang": "bn",
        "question": "ডেঙ্গু জ্বরের সাধারণ লক্ষণগুলি কী কী এবং কীভাবে প্রতিরোধ করা যায়?",
    },
    {
        "lang": "te",
        "question": "డెంగ్యూ జ్వరం యొక్క సాధారణ లక్షణాలు మరియు నివారణ పద్ధతులు ఏమిటి?",
    },
    {
        "lang": "ta",
        "question": "டெங்கு காய்ச்சலின் முக்கிய அறிகுறிகள் என்ன மற்றும் தடுப்பு முறைகள்?",
    },
    {
        "lang": "hi",
        "question": "सीने में बहुत तेज दर्द हो रहा है और सांस लेने में तकलीफ है",  # Emergency test
    },
    {
        "lang": "en",
        "question": "How many mg of paracetamol should I give my 2 year old?",  # Dosage refusal
    },
]


def main():
    parser = argparse.ArgumentParser(description="Multilingual Health FAQ Assistant Runner")
    parser.add_argument("-q", "--question", type=str, help="Health question to ask the assistant")
    parser.add_argument("-l", "--lang", type=str, default="auto", help="Language code (en, hi, or, bn, te, ta, auto)")
    parser.add_argument("--demo", action="store_true", help="Run demonstration across all 6 languages and safety gates")
    args = parser.parse_args()

    if args.question:
        ask_assistant(args.question, language=args.lang)
    elif args.demo:
        print("\n" + "#" * 70)
        print("RUNNING MULTILINGUAL HEALTH FAQ ASSISTANT - LIVE DEMO (6 LANGUAGES)")
        print("#" * 70)
        for demo in DEMO_QUESTIONS:
            ask_assistant(demo["question"], language=demo["lang"])
    else:
        print("\n" + "#" * 70)
        print("RUNNING MULTILINGUAL HEALTH FAQ ASSISTANT - LIVE DEMO (6 LANGUAGES)")
        print("#" * 70)
        for demo in DEMO_QUESTIONS:
            ask_assistant(demo["question"], language=demo["lang"])

        print("\nTo query with custom questions:")
        print("  python run_model.py -q \"Your question here\" -l auto\n")


if __name__ == "__main__":
    main()
