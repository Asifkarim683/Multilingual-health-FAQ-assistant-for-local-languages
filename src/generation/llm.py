"""Swappable LLM Provider interface supporting Gemini, OpenAI/Groq, and offline Mock."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import re
import requests


class LLMProvider(ABC):
    """Abstract Base Class for LLM generation providers."""

    @abstractmethod
    def generate(self, prompt: str, target_lang: str) -> str:
        """Generate response text from formatted prompt."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini API Provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model

    def generate(self, prompt: str, target_lang: str) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "maxOutputTokens": 1024,
            }
        }
        res = requests.post(url, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return "Unable to generate answer."
        text = candidates[0]["content"]["parts"][0]["text"]
        return text.strip()


class OpenAIProvider(LLMProvider):
    """OpenAI / Groq compatible API Provider."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model

    def generate(self, prompt: str, target_lang: str) -> str:
        if not self.api_key:
            raise ValueError("API key is not configured for OpenAI/Groq provider.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 800,
        }
        res = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"].strip()


class MockLLMProvider(LLMProvider):
    """
    Extractive grounded LLM mock for offline evaluation, development, and CI/CD.
    Synthesizes sentences from provided passages in the matching language, preserving citations.
    """

    def generate(self, prompt: str, target_lang: str) -> str:
        # Extract passages from prompt using clean regex
        passages = re.findall(
            r"--- \[Passage (\d+)\] Source: (.*?) \((.*?)\) \| Section: (.*?) ---\n(.*?)(?=(?:--- \[Passage|\n\nUSER QUESTION:|$))",
            prompt,
            re.DOTALL,
        )

        if not passages:
            if target_lang == "hi":
                return "मुझे अपने सत्यापित स्रोतों में इस प्रश्न की जानकारी नहीं मिली। [1]"
            elif target_lang == "or":
                return "ମୋର ସତ୍ୟାପିତ ସ୍ୱାସ୍ଥ୍ୟ ତଥ୍ୟରେ ଏହି ପ୍ରଶ୍ନର ଉତ୍ତର ମିଳିଲା ନାହିଁ। [1]"
            return "I could not find information on this topic in my verified public health sources. [1]"

        # Select most relevant sentences matching the target language or primary passage
        target_sentences = []
        cited_passages = []

        for p_idx, p_title, p_src, p_sec, p_text in passages:
            lines = [l.strip() for l in p_text.strip().split("\n") if l.strip()]
            for line in lines:
                # Basic language filter: check script
                if target_lang == "hi" and re.search(r"[\u0900-\u097F]", line):
                    target_sentences.append(line)
                    if p_idx not in cited_passages:
                        cited_passages.append(p_idx)
                elif target_lang == "or" and re.search(r"[\u0B00-\u0B7F]", line):
                    target_sentences.append(line)
                    if p_idx not in cited_passages:
                        cited_passages.append(p_idx)
                elif target_lang == "en" and not re.search(r"[\u0900-\u0D7F]", line):
                    target_sentences.append(line)
                    if p_idx not in cited_passages:
                        cited_passages.append(p_idx)

            if len(target_sentences) >= 3:
                break

        if not target_sentences:
            # Fallback to localized health guidance if passages were cross-lingual
            first_p = passages[0]
            cited_passages = [first_p[0]]
            if target_lang == "hi":
                target_sentences = ["सत्यापित सार्वजनिक स्वास्थ्य दिशा-निर्देशों के अनुसार उपयुक्त सावधानी और उपचार नियमों का पालन करें।"]
            elif target_lang == "or":
                target_sentences = ["ସତ୍ୟାପିତ ସାର୍ବଜନୀନ ସ୍ୱାସ୍ଥ୍ୟ ନିୟମ ଅନୁସାରେ ଉପଯୁକ୍ତ ସତର୍କତା ଓ ଡାକ୍ତରୀ ପରାମର୍ଶ ପାଳନ କରନ୍ତୁ।"]
            else:
                target_sentences = [l.strip() for l in first_p[4].strip().split("\n") if l.strip()][:2]

        citation_str = " ".join([f"[{cp}]" for cp in cited_passages]) or "[1]"
        body = " ".join(target_sentences[:3])
        return f"{body} {citation_str}"


def get_llm_provider(name: Optional[str] = None) -> LLMProvider:
    """Factory to get the appropriate LLM provider."""
    provider_name = (name or os.getenv("LLM_PROVIDER", "")).lower()

    if provider_name == "gemini" and os.getenv("GEMINI_API_KEY"):
        return GeminiProvider()
    elif provider_name in ["openai", "groq"] and (os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")):
        return OpenAIProvider()
    elif provider_name == "mock":
        return MockLLMProvider()

    # Automatic fallback: if Gemini key exists, use it; else use MockLLMProvider
    if os.getenv("GEMINI_API_KEY"):
        return GeminiProvider()
    return MockLLMProvider()
