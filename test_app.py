import pytest
from main import app
from extract_json import extract_json, ModelResponseStatus
from user_prompts import PROMPTS
from verify_json import verify_json_schema as verify_json

model_stats = {
    "total_tests": 0,
    "json_extraction_success": 0,
    "json_extraction_failed": 0,
    "json_verification_success": 0,
    "json_verification_failed": 0,
    "only_json": 0,
    "block_json": 0,
    "include_json": 0
}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("prompt", PROMPTS)
def test_get_valid_response(client, prompt):
    
    model_stats['total_tests'] += 1
    print("\nTest #" + str(model_stats['total_tests']))
    # send request to model and get response
    response = client.post('/getResponse', json={"prompt": prompt, "model": "mistral"})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['response'] != ""

    # extract json from response
    try:
        json_data, response_status = extract_json(data['response'])
        model_stats['json_extraction_success'] += 1
        
        if response_status == ModelResponseStatus.ONLY_JSON:
            model_stats['only_json'] += 1
        elif response_status == ModelResponseStatus.BLOCK_JSON:
            model_stats['block_json'] += 1
        elif response_status == ModelResponseStatus.INCLUDE_JSON:
            model_stats['include_json'] += 1
    except ValueError as e:
        model_stats['json_extraction_failed'] += 1
        pytest.fail(f"Failed to extract JSON from response: {e}")
        
    # verify json
    verified_json, error_message = verify_json(json_data)
    
    if not verified_json:
        model_stats['json_verification_failed'] += 1
        if error_message in model_stats:
            model_stats[error_message] += 1
        else:
            model_stats[error_message] = 1
        print(f"Failed to verify JSON: {error_message}")
        print(json_data)
        pytest.fail(f"Failed to verify JSON: {error_message}")
    else:
        model_stats['json_verification_success'] += 1
        assert verified_json == True

def teardown_module():
    print("\nModel Statistics:")
    for stat, number in model_stats.items():
        print(f"{stat}: {number}")
    print("\n\nModel Percentages:")
    for stat, number in model_stats.items():
        if stat == "total_tests":
            continue
        percentage = (number / model_stats['total_tests']) * 100
        print(f"{stat}: {percentage:.2f}%")
