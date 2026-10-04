import time
from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from automation.utils.logger import get_logger

logger = get_logger("DashboardPage")

class DashboardPage(BasePage):
    """Page Object for TestPilot Main Dashboard."""

    # Locators
    APP_TITLE = (By.CSS_SELECTOR, "[data-testid='app-title']")
    KPI_TOTAL_CASES = (By.CSS_SELECTOR, "[data-testid='kpi-total-cases']")
    KPI_TOTAL_RUNS = (By.CSS_SELECTOR, "[data-testid='kpi-total-runs']")
    KPI_PASSED_TESTS = (By.CSS_SELECTOR, "[data-testid='kpi-passed-tests']")
    KPI_FAILED_TESTS = (By.CSS_SELECTOR, "[data-testid='kpi-failed-tests']")
    KPI_PASS_RATE = (By.CSS_SELECTOR, "[data-testid='kpi-pass-rate']")
    
    BTN_RUN_TESTS = (By.CSS_SELECTOR, "[data-testid='btn-run-tests']")
    BTN_REFRESH = (By.CSS_SELECTOR, "[data-testid='btn-refresh']")
    BTN_NEW_TEST = (By.CSS_SELECTOR, "[data-testid='btn-new-test']")
    RUN_STATUS_BANNER = (By.CSS_SELECTOR, "[data-testid='run-status-banner']")

    INPUT_SEARCH = (By.CSS_SELECTOR, "[data-testid='input-search']")
    SELECT_STATUS_FILTER = (By.CSS_SELECTOR, "[data-testid='select-status-filter']")
    SELECT_TYPE_FILTER = (By.CSS_SELECTOR, "[data-testid='select-type-filter']")

    RESULTS_TABLE = (By.CSS_SELECTOR, "[data-testid='results-table']")
    RESULT_ROWS = (By.CSS_SELECTOR, "[data-testid='result-row']")
    RESULTS_EMPTY = (By.CSS_SELECTOR, "[data-testid='results-empty-state']")
    RUNS_TABLE = (By.CSS_SELECTOR, "[data-testid='runs-table']")
    RUN_ROWS = (By.CSS_SELECTOR, "[data-testid='run-row']")

    def open(self, base_url: str):
        self.navigate_to(base_url)
        self.wait_for_visible(*self.APP_TITLE)
        self.wait_for_visible(*self.RESULTS_TABLE)
        # Wait for data fetching to populate rows or show empty state
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.find_elements(*self.RESULT_ROWS)) > 0 or len(d.find_elements(*self.RESULTS_EMPTY)) > 0
            )
        except Exception:
            pass

    def is_dashboard_loaded(self) -> bool:
        return self.is_visible(*self.APP_TITLE) and self.is_visible(*self.KPI_TOTAL_CASES)

    def get_kpi_metrics(self) -> Dict[str, str]:
        """Reads all KPI metrics displayed on the dashboard."""
        return {
            "total_cases": self.get_text(*self.KPI_TOTAL_CASES),
            "total_runs": self.get_text(*self.KPI_TOTAL_RUNS),
            "passed_tests": self.get_text(*self.KPI_PASSED_TESTS),
            "failed_tests": self.get_text(*self.KPI_FAILED_TESTS),
            "pass_rate": self.get_text(*self.KPI_PASS_RATE),
        }

    def click_run_tests(self):
        """Triggers test suite execution via the dashboard Run Tests button."""
        logger.info("Triggering test suite run via UI button...")
        self.click(*self.BTN_RUN_TESTS)

    def wait_for_run_completion(self, timeout: int = 15):
        """Waits for execution status banner to report completion."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.RUN_STATUS_BANNER).is_displayed()
                and ("completed" in d.find_element(*self.RUN_STATUS_BANNER).text.lower()
                     or "failed" in d.find_element(*self.RUN_STATUS_BANNER).text.lower())
            )
        except Exception:
            self.wait_for_clickable(*self.BTN_RUN_TESTS, timeout=timeout)

    def search_results(self, term: str):
        """Enters search term into test results search bar."""
        self.enter_text(*self.INPUT_SEARCH, term)
        time.sleep(0.3)

    def filter_by_status(self, status: str):
        """Selects status filter (ALL, PASSED, FAILED)."""
        select_elem = self.wait_for_visible(*self.SELECT_STATUS_FILTER)
        select_elem.click()
        option_xpath = f"//select[@data-testid='select-status-filter']/option[@value='{status}']"
        self.driver.find_element(By.XPATH, option_xpath).click()
        time.sleep(0.3)

    def filter_by_type(self, test_type: str):
        """Selects type filter (ALL, API, UI)."""
        select_elem = self.wait_for_visible(*self.SELECT_TYPE_FILTER)
        select_elem.click()
        option_xpath = f"//select[@data-testid='select-type-filter']/option[@value='{test_type}']"
        self.driver.find_element(By.XPATH, option_xpath).click()
        time.sleep(0.3)

    def get_result_row_count(self) -> int:
        """Returns the number of visible rows in the test results table."""
        return len(self.find_elements(*self.RESULT_ROWS))

    def get_recent_runs_count(self) -> int:
        """Returns the number of recent runs displayed."""
        return len(self.find_elements(*self.RUN_ROWS))
