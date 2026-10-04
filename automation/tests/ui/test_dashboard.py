import pytest
from automation.pages.dashboard_page import DashboardPage
from automation.utils.logger import get_logger

logger = get_logger("test_dashboard")

@pytest.mark.ui
@pytest.mark.smoke
def test_dashboard_loads_and_displays_kpis(driver, frontend_base_url):
    """
    SDET UI Test 1: Verifies that TestPilot React dashboard loads cleanly,
    the header renders, and all 5 KPI summary cards display active metrics.
    """
    dashboard = DashboardPage(driver)
    logger.info(f"Opening dashboard at: {frontend_base_url}")
    dashboard.open(frontend_base_url)

    assert dashboard.is_dashboard_loaded(), "Dashboard failed to load or header/KPI cards are missing"
    
    metrics = dashboard.get_kpi_metrics()
    logger.info(f"Retrieved dashboard KPI metrics: {metrics}")
    
    # Assert KPI values are present
    assert metrics["total_cases"] != "", "Total Cases KPI card is empty"
    assert metrics["total_runs"] != "", "Total Runs KPI card is empty"
    assert "%" in metrics["pass_rate"] or metrics["pass_rate"].replace(".", "").isdigit(), "Invalid Pass Rate format"

@pytest.mark.ui
@pytest.mark.regression
def test_results_table_and_filtering(driver, frontend_base_url):
    """
    SDET UI Test 2: Verifies results table rows, status dropdown filter,
    and live keyword search.
    """
    dashboard = DashboardPage(driver)
    dashboard.open(frontend_base_url)

    initial_count = dashboard.get_result_row_count()
    logger.info(f"Initial results table row count: {initial_count}")
    assert initial_count > 0, "Expected seed results to be visible in table"

    # Test filtering by status: PASSED
    dashboard.filter_by_status("PASSED")
    passed_count = dashboard.get_result_row_count()
    logger.info(f"Row count after PASSED filter: {passed_count}")
    assert passed_count > 0, "Expected at least one PASSED test in table"

    # Test search filter
    dashboard.filter_by_status("ALL")
    dashboard.search_results("Health")
    searched_count = dashboard.get_result_row_count()
    logger.info(f"Row count after searching 'Health': {searched_count}")
    assert searched_count >= 1, "Expected matching row for 'Health'"

@pytest.mark.ui
def test_recent_runs_table_visible(driver, frontend_base_url):
    """
    SDET UI Test 3: Verifies that historical test runs table is rendered.
    """
    dashboard = DashboardPage(driver)
    dashboard.open(frontend_base_url)

    runs_count = dashboard.get_recent_runs_count()
    logger.info(f"Recent runs displayed: {runs_count}")
    assert runs_count > 0, "Expected at least one recent run record in the runs table"
