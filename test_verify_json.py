import pytest
from verify_json import verify_json_schema
from verify_json_test_cases import (
    VALID_TEST_CASES,
    MISSING_PROPERTY_TEST_CASES,
    MISPELLED_KEY_TEST_CASES,
    INCORRECT_TYPE_TEST_CASES,
    NON_POSITIVE_SIZE_TEST_CASES,
    OVERALL_FORMATTING_TEST_CASES
)

# --- Category 1: Valid JSON ---
@pytest.mark.parametrize("description,input_json", VALID_TEST_CASES)
def test_valid_json(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert valid, f"{description}: Expected valid JSON but got error: {error}"
    assert error is None

# --- Category 2: Missing Properties ---
@pytest.mark.parametrize("description,input_json", MISSING_PROPERTY_TEST_CASES)
def test_missing_property(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert not valid, f"{description}: Expected invalid JSON due to missing property but got {error}"
    assert error == "Missing property key in shape"

# --- Category 3: Mispelled Keys ---
@pytest.mark.parametrize("description,input_json", MISPELLED_KEY_TEST_CASES)
def test_mispelled_keys(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert not valid, f"{description}: Expected invalid JSON due to mispelled key"
    assert error == "Mispelled key in JSON"

# --- Category 4: Incorrect Value Types ---
@pytest.mark.parametrize("description,input_json", INCORRECT_TYPE_TEST_CASES)
def test_incorrect_type(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert not valid, f"{description}: Expected invalid JSON due to incorrect type"
    assert error == "Invalid type error"
    
# --- Category 5: Non-Positive Size Values ---
@pytest.mark.parametrize("description,input_json", NON_POSITIVE_SIZE_TEST_CASES)
def test_non_positive_size_values(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert not valid, f"{description}: Expected invalid JSON due to non-positive size values"
    assert error == "Non-positive size value"

# --- Category 6: Incorrect Overall Formatting ---
@pytest.mark.parametrize("description,input_json", OVERALL_FORMATTING_TEST_CASES)
def test_incorrect_overall_formatting(description, input_json):
    valid, error = verify_json_schema(input_json)
    assert not valid, f"{description}: Expected invalid JSON due to overall formatting"
    assert error == "Overall formatting is incorrect"
