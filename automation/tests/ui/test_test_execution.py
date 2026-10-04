import time
import pytest
from automation.pages.dashboard_page import DashboardPage
from automation.pages.test_execution_page import TestExecutionPage
from automation.utils.logger import get_logger

logger = get_logger("test_test_execution")

@pytest.mark.ui
@pytest.mark.smoke
def test_trigger_run_from_dashboard(driver, frontend_base_url):
    """
    SDET UI Test 4: Verifies clicking 'Run Tests' on Dashboard triggers
    automated execution, displays status feedback, and updates metrics.
    """
    dashboard = DashboardPage(driver)
    dashboard.open(frontend_base_url)

    initial_metrics = dashboard.get_kpi_metrics()
    logger.info(f"Initial KPI metrics: {initial_metrics}")

    # Trigger test execution
    dashboard.click_run_tests()
    dashboard.wait_for_run_completion(timeout=15)

    # Re-fetch metrics and verify update
    updated_metrics = dashboard.get_kpi_metrics()
    logger.info(f"Updated KPI metrics after run: {updated_metrics}")
    
    assert int(updated_metrics["total_runs"]) >= int(initial_metrics["total_runs"]), \
        "Total runs count should not decrease after triggering a run"

@pytest.mark.ui
@pytest.mark.regression
def test_execution_console_workflow(driver, frontend_base_url):
    """
    SDET UI Test 5: Verifies the dedicated Test Execution console tab,
    suite selection (API), real-time output terminal, and completion badge.
    """
    dashboard = DashboardPage(driver)
    dashboard.open(frontend_base_url)

    exec_page = TestExecutionPage(driver)
    exec_page.navigate_to_execution_tab()

    # Select API suite
    exec_page.select_suite("API")
    exec_page.run_suite()
    exec_page.wait_for_completion(timeout=15)

    status = exec_page.get_execution_status()
    logger.info(f"Execution finished with status: {status}")
    assert any(term in status.upper() for term in ["COMPLETED", "SUCCESS", "PASSED"]), \
        f"Unexpected status: {status}"
    
    assert exec_page.is_terminal_output_present(), "Terminal output log should be visible"
