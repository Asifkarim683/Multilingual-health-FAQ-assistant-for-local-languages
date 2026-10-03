"""Centralized Language Registry Loader and Validator."""
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import yaml

REQUIRED_LANGUAGE_FIELDS = [
    "code",
    "name",
    "native_name",
    "script",
    "font",
    "status",
    "emergency_keywords",
    "disclaimer",
    "example_questions",
    "eval_file",
    "ui_strings",
]

REQUIRED_UI_STRINGS = [
    "title",
    "tagline",
    "placeholder",
    "ask_button",
    "sources_heading",
    "disclaimer_label",
    "emergency_badge",
    "emergency_message",
    "refusal_out_of_scope",
    "refusal_dosage",
    "status_stable",
    "status_experimental",
]

VALID_STATUSES = {"stable", "experimental"}


class RegistryValidationError(ValueError):
    """Raised when a language registry configuration violates schema requirements."""
    pass


def validate_language_entry(entry: Dict[str, Any]) -> None:
    """Validate that a single language entry has all required fields and valid values."""
    if not isinstance(entry, dict):
        raise RegistryValidationError(f"Language entry must be a dictionary, got {type(entry).__name__}")

    lang_code = entry.get("code", "unknown")

    # 1. Check required top-level fields
    for field in REQUIRED_LANGUAGE_FIELDS:
        if field not in entry:
            raise RegistryValidationError(
                f"Language '{lang_code}' is missing required field: '{field}'"
            )
        if entry[field] is None or (isinstance(entry[field], (str, list, dict)) and len(entry[field]) == 0):
            raise RegistryValidationError(
                f"Language '{lang_code}' has empty value for required field: '{field}'"
            )

    # 2. Check status validity
    if entry["status"] not in VALID_STATUSES:
        raise RegistryValidationError(
            f"Language '{lang_code}' has invalid status '{entry['status']}'. Must be one of: {sorted(VALID_STATUSES)}"
        )

    # 3. Check emergency_keywords
    if not isinstance(entry["emergency_keywords"], list):
        raise RegistryValidationError(
            f"Language '{lang_code}' 'emergency_keywords' must be a list, got {type(entry['emergency_keywords']).__name__}"
        )
    for idx, kw in enumerate(entry["emergency_keywords"]):
        if not isinstance(kw, str) or not kw.strip():
            raise RegistryValidationError(
                f"Language '{lang_code}' emergency keyword at index {idx} must be a non-empty string"
            )

    # 4. Check example_questions
    if not isinstance(entry["example_questions"], list):
        raise RegistryValidationError(
            f"Language '{lang_code}' 'example_questions' must be a list, got {type(entry['example_questions']).__name__}"
        )

    # 5. Check ui_strings
    ui_strings = entry["ui_strings"]
    if not isinstance(ui_strings, dict):
        raise RegistryValidationError(
            f"Language '{lang_code}' 'ui_strings' must be a dictionary, got {type(ui_strings).__name__}"
        )
    for ui_key in REQUIRED_UI_STRINGS:
        if ui_key not in ui_strings:
            raise RegistryValidationError(
                f"Language '{lang_code}' ui_strings is missing required key: '{ui_key}'"
            )
        if not isinstance(ui_strings[ui_key], str) or not ui_strings[ui_key].strip():
            raise RegistryValidationError(
                f"Language '{lang_code}' ui_strings key '{ui_key}' must be a non-empty string"
            )


def load_languages_registry(
    config_path: Union[str, Path] = Path("config/languages.yaml"),
    validate: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """
    Load all configured languages from languages.yaml.
    Validates schema for each language if validate=True.
    Returns mapping of lang_code -> language config dict.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Language configuration file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "languages" not in data:
        raise RegistryValidationError(f"Invalid languages config: root must be dict with 'languages' list.")

    languages_list = data.get("languages", [])
    if not isinstance(languages_list, list) or len(languages_list) == 0:
        raise RegistryValidationError("Language configuration must define at least one language.")

    registry: Dict[str, Dict[str, Any]] = {}
    for entry in languages_list:
        if validate:
            validate_language_entry(entry)
        code = entry["code"]
        if code in registry:
            raise RegistryValidationError(f"Duplicate language code found in registry: '{code}'")
        registry[code] = entry

    return registry


def get_language(
    code: str,
    config_path: Union[str, Path] = Path("config/languages.yaml"),
) -> Optional[Dict[str, Any]]:
    """Retrieve configuration for a specific language code."""
    registry = load_languages_registry(config_path, validate=False)
    return registry.get(code)


def get_supported_language_codes(
    config_path: Union[str, Path] = Path("config/languages.yaml"),
    status: Optional[str] = None,
) -> List[str]:
    """Retrieve list of supported language codes, optionally filtered by status ('stable' or 'experimental')."""
    registry = load_languages_registry(config_path, validate=False)
    if status is None:
        return list(registry.keys())
    return [code for code, info in registry.items() if info.get("status") == status]
