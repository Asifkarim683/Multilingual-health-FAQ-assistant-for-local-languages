"""Safety guardrails module for emergency detection, dosage/diagnosis refusal, and confidence filtering."""
from .emergency import check_emergency, EmergencyResult
from .dosage_diagnosis import check_dosage_or_diagnosis, DosageRefusalResult
from .confidence import check_retrieval_confidence, ConfidenceResult
from .guardrails import SafetyGuardrail, SafetyCheckResult

__all__ = [
    "check_emergency",
    "EmergencyResult",
    "check_dosage_or_diagnosis",
    "DosageRefusalResult",
    "check_retrieval_confidence",
    "ConfidenceResult",
    "SafetyGuardrail",
    "SafetyCheckResult",
]
