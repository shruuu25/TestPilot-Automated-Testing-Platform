import pytest
import requests
from automation.utils.logger import get_logger

logger = get_logger("test_health")

@pytest.mark.api
@pytest.mark.smoke
def test_root_endpoint(api_base_url):
    """
    Smoke Test: Verifies root service endpoint responds with 200 OK
    and accurate service metadata.
    """
    logger.info(f"Testing root endpoint at: {api_base_url}/")
    response = requests.get(f"{api_base_url}/")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "running"
    assert "docs" in data
    assert "version" in data
    logger.info("Root endpoint verification passed.")

@pytest.mark.api
@pytest.mark.smoke
def test_health_endpoint(api_base_url):
    """
    Health Check Test: Verifies /health endpoint returns HTTP 200
    and database connectivity state is healthy.
    """
    logger.info(f"Testing health endpoint at: {api_base_url}/health")
    response = requests.get(f"{api_base_url}/health")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "connected" in data["database"].lower()
    assert data["version"] == "1.0.0"
    logger.info("Health check endpoint verification passed.")
