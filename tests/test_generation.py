"""Unit tests for generation, citations, language verification, and grounded responses."""
import pytest
from src.generation.citation import extract_citations, Citation
from src.generation.language_verifier import detect_script_language, verify_language_match
from src.generation.generator import GroundedGenerator, GenerationResult
from src.generation.llm import MockLLMProvider


def test_detect_script_language():
    assert detect_script_language("What are dengue symptoms?") == "en"
    assert detect_script_language("डेंगू बुखार के लक्षण क्या हैं?") == "hi"
    assert detect_script_language("ଡେଙ୍ଗୁ ଜ୍ୱରର ଲକ୍ଷଣ କ'ଣ?") == "or"


def test_verify_language_match():
    assert verify_language_match("This is clear English advice.", "en")[0] is True
    assert verify_language_match("डेंगू एडीज मच्छर से फैलता है।", "hi")[0] is True
    assert verify_language_match("ଡେଙ୍ଗୁ ଏକ ଭୂତାଣୁଜନିତ ରୋଗ।", "or")[0] is True
    # Mismatch
    assert verify_language_match("This is English.", "hi")[0] is False


def test_extract_citations():
    retrieved_chunks = [
        {"title": "Dengue WHO", "url": "https://who.int/dengue", "section": "Symptoms"},
        {"title": "Dengue NVBDCP", "url": "https://nvbdcp.gov.in", "section": "Prevention"},
        {"title": "Dengue WHO", "url": "https://who.int/dengue", "section": "Symptoms"},  # Duplicate URL
    ]
    citations = extract_citations("Here is the answer [1] [2]", retrieved_chunks)
    assert len(citations) == 2
    assert citations[0].id == 1
    assert citations[0].url == "https://who.int/dengue"
    assert citations[1].id == 2
    assert citations[1].url == "https://nvbdcp.gov.in"


def test_grounded_generator_multilingual_flow():
    generator = GroundedGenerator(llm_provider=MockLLMProvider())

    sample_chunks = [
        {
            "source_id": "SRC-01",
            "title": "Dengue Guidelines",
            "url": "https://who.int/dengue",
            "section": "Symptoms",
            "text": "Common symptoms of dengue include sudden high fever, severe headache, and joint pain.",
            "language": "en",
        },
        {
            "source_id": "SRC-01-HI",
            "title": "डेंगू लक्षण",
            "url": "https://nvbdcp.gov.in",
            "section": "लक्षण",
            "text": "डेंगू के मुख्य लक्षण: तेज बुखार, सिरदर्द, जोड़ों और मांसपेशियों में तेज दर्द।",
            "language": "hi",
        },
        {
            "source_id": "SRC-01-OR",
            "title": "ଡେଙ୍ଗୁ ଲକ୍ଷଣ",
            "url": "http://nrhmorissa.gov.in",
            "section": "ଲକ୍ଷଣ",
            "text": "ଡେଙ୍ଗୁର ପ୍ରମୁଖ ଲକ୍ଷଣ: ହଠାତ୍ ପ୍ରବଳ ଜ୍ୱର, ମୁଣ୍ଡବିନ୍ଧା ଏବଂ ଗଣ୍ଠି ବିନ୍ଧା।",
            "language": "or",
        },
    ]

    # Test EN
    res_en = generator.generate_response("What are dengue symptoms?", sample_chunks, "en")
    assert res_en.status == "answered"
    assert len(res_en.citations) > 0
    assert "disclaimer" in res_en.to_dict()
    assert res_en.language == "en"

    # Test HI
    res_hi = generator.generate_response("डेंगू के लक्षण क्या हैं?", sample_chunks, "hi")
    assert res_hi.status == "answered"
    assert len(res_hi.citations) > 0
    assert res_hi.language == "hi"

    # Test OR
    res_or = generator.generate_response("ଡେଙ୍ଗୁ ଜ୍ୱରର ଲକ୍ଷଣ କ'ଣ?", sample_chunks, "or")
    assert res_or.status == "answered"
    assert len(res_or.citations) > 0
    assert res_or.language == "or"


def test_ten_sample_questions_with_citations():
    """Pass check for Part 3: 10 sample questions return answers with valid citations."""
    generator = GroundedGenerator(llm_provider=MockLLMProvider())

    questions = [
        ("What are symptoms of dengue?", "en"),
        ("How to prevent diabetes?", "en"),
        ("What is the immunization schedule?", "en"),
        ("डेंगू बुखार के क्या लक्षण हैं?", "hi"),
        ("डायबिटीज में क्या खाएं?", "hi"),
        ("ओआरएस कैसे बनाएं?", "hi"),
        ("ଡେଙ୍ଗୁ ରୋଗର ଲକ୍ଷଣ କ'ଣ?", "or"),
        ("ମଧୁମେହ ନିୟନ୍ତ୍ରଣ କିପରି କରିବା?", "or"),
        ("ଶିଶୁର ଟିକା କେବେ ଦିଆଯାଏ?", "or"),
        ("ଓଆରଏସ୍ କିପରି ପ୍ରସ୍ତୁତ କରିବା?", "or"),
    ]

    sample_chunks = [
        {
            "source_id": "SRC-01",
            "title": "Health Guide",
            "url": "https://mohfw.gov.in",
            "section": "General",
            "text": "Dengue causes fever. डेंगू में बुखार होता है। ଡେଙ୍ଗୁରେ ଜ୍ୱର ହୁଏ।",
            "language": "en",
        }
    ]

    for q, lang in questions:
        res = generator.generate_response(q, sample_chunks, lang)
        assert res.status == "answered"
        assert len(res.citations) >= 1
        assert res.citations[0]["url"] == "https://mohfw.gov.in"
        assert len(res.disclaimer) > 10
