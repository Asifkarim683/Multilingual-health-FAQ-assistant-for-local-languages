"""Unit tests for Language Registry validation schema and loader."""
import pytest
import copy
import yaml
from pathlib import Path

from src.registry import (
    load_languages_registry,
    validate_language_entry,
    get_language,
    get_supported_language_codes,
    RegistryValidationError,
    REQUIRED_LANGUAGE_FIELDS,
    REQUIRED_UI_STRINGS,
)


@pytest.fixture
def valid_entry():
    return {
        "code": "test_lang",
        "name": "Test Language",
        "native_name": "Native Test",
        "script": "Latin",
        "font": "Inter, sans-serif",
        "status": "experimental",
        "emergency_keywords": ["chest pain", "heart attack"],
        "disclaimer": "Medical disclaimer for testing purposes.",
        "example_questions": ["What are the symptoms of fever?"],
        "eval_file": "data/eval/test.csv",
        "ui_strings": {
            "title": "Health Assistant",
            "tagline": "Verified health info",
            "placeholder": "Ask something...",
            "ask_button": "Ask",
            "sources_heading": "Sources",
            "disclaimer_label": "Disclaimer",
            "emergency_badge": "Emergency",
            "emergency_message": "Call 112 immediately",
            "refusal_out_of_scope": "No information found",
            "refusal_dosage": "Cannot prescribe dosage",
            "status_stable": "Verified",
            "status_experimental": "Experimental",
        },
    }


def test_registry_loads_current_config():
    """Verify production config/languages.yaml loads and validates completely."""
    registry = load_languages_registry(Path("config/languages.yaml"), validate=True)
    assert len(registry) >= 3
    assert "en" in registry
    assert "hi" in registry
    assert "or" in registry

    for code, info in registry.items():
        assert info["status"] in {"stable", "experimental"}
        assert len(info["emergency_keywords"]) > 0
        assert len(info["disclaimer"]) > 10
        assert len(info["ui_strings"]) >= len(REQUIRED_UI_STRINGS)


def test_registry_valid_entry(valid_entry):
    """Verify a complete valid entry passes validation without error."""
    validate_language_entry(valid_entry)


@pytest.mark.parametrize("missing_field", REQUIRED_LANGUAGE_FIELDS)
def test_registry_missing_required_field_raises_error(valid_entry, missing_field):
    """
    PRD Part 10 Pass Check:
    Removing any required field from a registry entry MUST fail validation.
    """
    entry = copy.deepcopy(valid_entry)
    del entry[missing_field]

    with pytest.raises(RegistryValidationError) as exc_info:
        validate_language_entry(entry)

    assert missing_field in str(exc_info.value)


@pytest.mark.parametrize("empty_field", ["code", "name", "native_name", "script", "font", "status", "disclaimer", "eval_file"])
def test_registry_empty_string_field_raises_error(valid_entry, empty_field):
    """Empty string values for mandatory fields must fail."""
    entry = copy.deepcopy(valid_entry)
    entry[empty_field] = ""

    with pytest.raises(RegistryValidationError) as exc_info:
        validate_language_entry(entry)

    assert empty_field in str(exc_info.value)


@pytest.mark.parametrize("missing_ui_key", REQUIRED_UI_STRINGS)
def test_registry_missing_ui_string_raises_error(valid_entry, missing_ui_key):
    """Removing any required ui_string must fail validation."""
    entry = copy.deepcopy(valid_entry)
    del entry["ui_strings"][missing_ui_key]

    with pytest.raises(RegistryValidationError) as exc_info:
        validate_language_entry(entry)

    assert missing_ui_key in str(exc_info.value)


def test_registry_invalid_status_raises_error(valid_entry):
    """Status must be either 'stable' or 'experimental'."""
    entry = copy.deepcopy(valid_entry)
    entry["status"] = "in_progress"

    with pytest.raises(RegistryValidationError) as exc_info:
        validate_language_entry(entry)

    assert "invalid status" in str(exc_info.value).lower()


def test_registry_empty_emergency_keywords_raises_error(valid_entry):
    """Empty emergency_keywords list or empty keyword string must fail."""
    entry = copy.deepcopy(valid_entry)
    entry["emergency_keywords"] = []

    with pytest.raises(RegistryValidationError):
        validate_language_entry(entry)

    entry["emergency_keywords"] = ["   "]
    with pytest.raises(RegistryValidationError):
        validate_language_entry(entry)


def test_registry_duplicate_code_raises_error(tmp_path, valid_entry):
    """Duplicate language codes in languages.yaml must fail."""
    dup_config = {
        "languages": [
            valid_entry,
            copy.deepcopy(valid_entry),
        ]
    }
    config_file = tmp_path / "languages.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(dup_config, f)

    with pytest.raises(RegistryValidationError) as exc_info:
        load_languages_registry(config_file, validate=True)

    assert "Duplicate language code" in str(exc_info.value)


def test_pass_check_removing_field_from_temp_yaml_fails(tmp_path):
    """
    Explicit pass check: removing a field from an entry in a YAML file
    causes load_languages_registry to fail.
    """
    with open("config/languages.yaml", "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # Remove 'disclaimer' from the first language
    broken_data = copy.deepcopy(raw)
    del broken_data["languages"][0]["disclaimer"]

    temp_file = tmp_path / "broken_languages.yaml"
    with open(temp_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(broken_data, f)

    with pytest.raises(RegistryValidationError) as exc_info:
        load_languages_registry(temp_file, validate=True)

    assert "disclaimer" in str(exc_info.value)


def test_get_supported_language_codes():
    """Verify helper retrieves all or status-filtered codes."""
    all_codes = get_supported_language_codes()
    assert "en" in all_codes
    assert "hi" in all_codes
    assert "or" in all_codes

    stable_codes = get_supported_language_codes(status="stable")
    assert "en" in stable_codes
    assert "hi" in stable_codes
    assert "or" in stable_codes
