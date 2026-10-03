"""API contract and endpoint integration tests."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["total_chunks"] > 0
    assert "en" in data["supported_languages"]
    assert "hi" in data["supported_languages"]
    assert "or" in data["supported_languages"]


def test_languages_endpoint():
    response = client.get("/api/languages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    codes = [l["code"] for l in data]
    assert "en" in codes
    assert "hi" in codes
    assert "or" in codes


def test_ask_valid_question_english():
    payload = {
        "question": "What are the common symptoms of dengue fever?",
        "language": "en",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert len(data["answer"]) > 10
    assert len(data["citations"]) >= 1
    assert "disclaimer" in data
    assert data["language"] == "en"
    assert "request_id" in data


def test_ask_valid_question_hindi():
    payload = {
        "question": "डेंगू बुखार के मुख्य लक्षण क्या हैं?",
        "language": "hi",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert len(data["citations"]) >= 1
    assert data["language"] == "hi"


def test_ask_valid_question_odia():
    payload = {
        "question": "ଡେଙ୍ଗୁ ଜ୍ୱରର ପ୍ରମୁଖ ଲକ୍ଷଣଗୁଡ଼ିକ କ'ଣ?",
        "language": "or",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert len(data["citations"]) >= 1
    assert data["language"] == "or"


def test_ask_emergency_handling():
    payload = {
        "question": "My grandfather has severe chest pain and cannot breathe",
        "language": "en",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "emergency"
    assert "112" in data["answer"] or "emergency" in data["answer"].lower()
    assert len(data["citations"]) == 0


def test_ask_dosage_refusal():
    payload = {
        "question": "How many mg of paracetamol tablet should I take?",
        "language": "en",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert "cannot provide medication dosage" in data["answer"].lower()


def test_ask_out_of_scope_refusal():
    payload = {
        "question": "Who won the cricket match yesterday in Mumbai?",
        "language": "en",
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"


def test_ask_invalid_input_schema():
    # Empty question
    response = client.post("/api/ask", json={"question": ""})
    assert response.status_code == 422


def test_feedback_submission():
    payload = {
        "request_id": "test-req-12345",
        "rating": "up",
        "comment": "Very clear dengue symptoms explanation.",
    }
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_tts_endpoint_valid_audio():
    response = client.get("/api/tts?text=Drink%20plenty%20of%20clean%20water.&language=en")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert len(response.content) > 1000


def test_tts_endpoint_empty_text():
    response = client.get("/api/tts?text=")
    assert response.status_code == 400

