import pytest
from extract_json import extract_json, ModelResponseStatus

def test_extract_json_code_block_valid_json():
    response = (
        "Hello! Here is your output:\n"
        "```json\n"
        '{"test": "value", "number": 42}\n'
        "```\n"
        "Hope this helps!"
    )
    result, status = extract_json(response)
    expected = {"test": "value", "number": 42}
    assert result == expected
    assert status == ModelResponseStatus.BLOCK_JSON

def test_extract_json_code_block_invalid_json():
    response = (
        "Greetings!\n"
        "```json\n"
        '{"test": "value, "number": 42,}\n'
        "```\n"
        "Please check the data."
    )
    with pytest.raises(ValueError) as excinfo:
        extract_json(response)
    assert "Regex extraction succeeded, but JSON decoding failed" in str(excinfo.value)

def test_extract_json_no_code_block_valid_json():
    response = (
        "The result is as follows:\n"
        "Here is the data: {\"test\": \"value\", \"status\": \"ok\"}\n"
        "Thank you for using our service."
    )
    result, status = extract_json(response)
    expected = {"test": "value", "status": "ok"}
    assert result == expected
    assert status == ModelResponseStatus.INCLUDE_JSON

def test_extract_json_no_code_block_invalid_json():
    response = (
        "I'm sorry, but I couldn't generate a proper JSON response based on your input. Please try again."
    )
    with pytest.raises(ValueError) as excinfo:
        extract_json(response)
    assert "Failed to locate valid JSON" in str(excinfo.value)

def test_extract_json_only():
    response = (
        """{"shapes":[{"shape": "Cube", "size": {"x": 1, "y": 1, "z": 1}, "position": {"x": 0, "y": 0, "z": 0}}]}"""
    )
    result, status = extract_json(response)
    expected = {"shapes": [{"shape": "Cube", "size": {"x": 1, "y": 1, "z": 1}, "position": {"x": 0, "y": 0, "z": 0}}]}
    assert result == expected
    assert status == ModelResponseStatus.ONLY_JSON
