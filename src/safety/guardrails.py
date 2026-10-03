"""Unified safety guardrails coordinating pre-retrieval and post-retrieval safety gates."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path

from .emergency import check_emergency, EmergencyResult
from .dosage_diagnosis import check_dosage_or_diagnosis, DosageRefusalResult
from .confidence import check_retrieval_confidence, ConfidenceResult


@dataclass
class SafetyCheckResult:
    action: str  # 'proceed' | 'emergency' | 'refused'
    reason: Optional[str]
    message: str


class SafetyGuardrail:
    """End-to-end safety guardrail orchestrator."""

    def __init__(self, config_path: Path = Path("config/languages.yaml")):
        self.config_path = config_path

    def run_pre_check(self, query: str, language: str = "en") -> SafetyCheckResult:
        """
        Execute pre-retrieval checks:
        1. Emergency detection
        2. Dosage and clinical diagnosis refusal
        """
        # 1. Emergency Check (Highest Priority)
        em_res = check_emergency(query=query, language=language, config_path=self.config_path)
        if em_res.is_emergency:
            return SafetyCheckResult(
                action="emergency",
                reason=f"emergency_keyword:{em_res.matched_keyword}",
                message=em_res.emergency_message,
            )

        # 2. Dosage & Diagnosis Refusal
        dd_res = check_dosage_or_diagnosis(query=query, language=language)
        if dd_res.is_refusal:
            return SafetyCheckResult(
                action="refused",
                reason=dd_res.reason,
                message=dd_res.refusal_message,
            )

        return SafetyCheckResult(
            action="proceed",
            reason=None,
            message="",
        )

    def run_post_retrieval_check(
        self,
        search_results: List[Any],
        language: str = "en",
        threshold: Optional[float] = None,
    ) -> SafetyCheckResult:
        """
        Execute post-retrieval confidence check.
        Triggers refusal if retrieved chunks have insufficient confidence.
        """
        conf_res = check_retrieval_confidence(
            search_results=search_results,
            language=language,
            threshold=threshold,
        )
        if not conf_res.is_sufficient:
            return SafetyCheckResult(
                action="refused",
                reason="low_confidence_out_of_scope",
                message=conf_res.refusal_message,
            )

        return SafetyCheckResult(
            action="proceed",
            reason=None,
            message="",
        )
