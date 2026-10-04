import pytest
import requests
from automation.utils.logger import get_logger
from backend.app.models import TestRun, TestResult

logger = get_logger("test_results_api")

@pytest.mark.api
@pytest.mark.smoke
def test_get_runs_list(api_base_url):
    """Verifies GET /api/runs returns historical execution runs."""
    url = f"{api_base_url}/api/runs"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    runs = response.json()
    assert isinstance(runs, list)
    assert len(runs) > 0, "At least one seed run should be present"
    
    first = runs[0]
    for key in ["id", "started_at", "total_tests", "passed_tests", "failed_tests", "status"]:
        assert key in first

@pytest.mark.api
def test_get_results_list(api_base_url):
    """Verifies GET /api/results returns list of test outcomes."""
    url = f"{api_base_url}/api/results"
    response = requests.get(url)
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0
    first = results[0]
    for key in ["id", "test_run_id", "test_case_id", "status", "duration"]:
        assert key in first

@pytest.mark.api
@pytest.mark.regression
def test_trigger_new_test_run(api_base_url, db_session):
    """
    Validates triggering a complete test suite execution via POST /api/runs.
    Confirms that results are collected, metrics computed, and persisted to the database.
    """
    url = f"{api_base_url}/api/runs"
    payload = {"test_type": "API"}
    logger.info(f"Triggering test execution run via POST {url}")
    
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    
    run_data = response.json()
    run_id = run_data["id"]
    assert run_id > 0
    assert run_data["status"] in ("COMPLETED", "FAILED", "RUNNING")
    assert run_data["total_tests"] > 0
    assert "results" in run_data
    assert len(run_data["results"]) == run_data["total_tests"]

    # Direct Database Verification
    db_run = db_session.query(TestRun).filter(TestRun.id == run_id).first()
    assert db_run is not None, f"TestRun {run_id} missing from database"
    assert db_run.total_tests == run_data["total_tests"]

    db_results = db_session.query(TestResult).filter(TestResult.test_run_id == run_id).all()
    assert len(db_results) == run_data["total_tests"]
    logger.info(f"Test run {run_id} and {len(db_results)} results confirmed in SQL database.")

@pytest.mark.api
def test_get_run_by_id(api_base_url):
    """Verifies retrieving specific test run details with results."""
    # List runs to get a valid run ID
    runs_res = requests.get(f"{api_base_url}/api/runs")
    assert runs_res.status_code == 200
    valid_id = runs_res.json()[0]["id"]

    response = requests.get(f"{api_base_url}/api/runs/{valid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == valid_id
    assert "results" in data
    assert isinstance(data["results"], list)

@pytest.mark.api
def test_get_nonexistent_run_returns_404(api_base_url):
    """Negative Test: Verifies GET /api/runs/999999 returns HTTP 404."""
    response = requests.get(f"{api_base_url}/api/runs/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.api
def test_get_nonexistent_result_returns_404(api_base_url):
    """Negative Test: Verifies GET /api/results/999999 returns HTTP 404."""
    response = requests.get(f"{api_base_url}/api/results/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.api
@pytest.mark.smoke
def test_get_dashboard_stats(api_base_url):
    """Verifies aggregated metrics endpoint for dashboard KPIs."""
    url = f"{api_base_url}/api/stats"
    response = requests.get(url)
    assert response.status_code == 200
    stats = response.json()
    for k in ["total_test_cases", "total_test_runs", "total_passed_tests", "total_failed_tests", "pass_percentage"]:
        assert k in stats
        assert stats[k] >= 0
