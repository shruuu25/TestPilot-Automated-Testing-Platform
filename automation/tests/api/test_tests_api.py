import pytest
import requests
from automation.utils.logger import get_logger
from automation.utils.helpers import generate_random_test_payload
from backend.app.models import TestCase

logger = get_logger("test_tests_api")

@pytest.mark.api
@pytest.mark.regression
def test_get_all_tests(api_base_url):
    """Verifies GET /api/tests returns array of registered test definitions."""
    url = f"{api_base_url}/api/tests"
    logger.info(f"Executing GET: {url}")
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response body must be a list"
    assert len(data) > 0, "Initial seed tests should be present"
    
    first_item = data[0]
    for required_key in ["id", "name", "test_type", "endpoint_or_url", "created_at"]:
        assert required_key in first_item, f"Missing key: {required_key}"

@pytest.mark.api
@pytest.mark.smoke
def test_create_test_case_success(api_base_url, db_session):
    """
    Validates POST /api/tests with valid payload creates a test case (HTTP 201).
    Performs direct database validation to confirm row insertion.
    """
    payload = generate_random_test_payload(test_type="API", prefix="RegressionTest")
    url = f"{api_base_url}/api/tests"
    logger.info(f"Executing POST: {url} with payload {payload}")
    
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}: {response.text}"
    
    created = response.json()
    assert created["id"] > 0
    assert created["name"] == payload["name"]
    assert created["test_type"] == "API"
    assert created["endpoint_or_url"] == payload["endpoint_or_url"]

    # SDET Database Validation: Verify persistence in SQL database directly
    db_record = db_session.query(TestCase).filter(TestCase.id == created["id"]).first()
    assert db_record is not None, f"Database assertion failed: record {created['id']} not found in DB"
    assert db_record.name == payload["name"]
    logger.info(f"Database validation verified successfully for test case id: {created['id']}")

@pytest.mark.api
def test_get_test_case_by_id(api_base_url):
    """Verifies fetching an existing test definition by valid primary key."""
    # First create a test case to ensure isolation
    payload = generate_random_test_payload(test_type="UI", prefix="FetchById")
    create_res = requests.post(f"{api_base_url}/api/tests", json=payload)
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # Fetch by ID
    get_res = requests.get(f"{api_base_url}/api/tests/{created_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == created_id
    assert data["name"] == payload["name"]

@pytest.mark.api
def test_get_nonexistent_test_returns_404(api_base_url):
    """Negative Scenario: Verifies GET /api/tests/999999 returns HTTP 404."""
    non_existent_id = 999999
    url = f"{api_base_url}/api/tests/{non_existent_id}"
    logger.info(f"Executing negative GET test: {url}")
    response = requests.get(url)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.api
@pytest.mark.parametrize("invalid_payload,expected_field", [
    ({"test_type": "API", "endpoint_or_url": "/api/v1"}, "name"),
    ({"name": "No Type", "endpoint_or_url": "/api/v1"}, "test_type"),
    ({"name": "Bad Type", "test_type": "GRAPHQL", "endpoint_or_url": "/api/v1"}, "test_type"),
    ({"name": "   ", "test_type": "API", "endpoint_or_url": "/api/v1"}, "name"),
])
def test_create_test_case_invalid_payload_returns_422(api_base_url, invalid_payload, expected_field):
    """
    Negative Scenarios: Parameterized test verifying malformed or invalid
    payloads result in HTTP 422 Unprocessable Entity.
    """
    url = f"{api_base_url}/api/tests"
    logger.info(f"Executing negative POST validation with payload: {invalid_payload}")
    response = requests.post(url, json=invalid_payload)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}: {response.text}"
    logger.info(f"Validation rejection confirmed for invalid input on field '{expected_field}'")

@pytest.mark.api
@pytest.mark.parametrize("target_type", ["API", "UI"])
def test_filter_tests_by_type(api_base_url, target_type):
    """Verifies query param filter ?test_type= works accurately for API and UI."""
    url = f"{api_base_url}/api/tests?test_type={target_type}"
    response = requests.get(url)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    for item in items:
        assert item["test_type"] == target_type, f"Expected {target_type}, got {item['test_type']}"
