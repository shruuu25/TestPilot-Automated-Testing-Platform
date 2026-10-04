import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from automation.utils.logger import get_logger

logger = get_logger("TestExecutionPage")

class TestExecutionPage(BasePage):
    """Page Object for TestPilot Test Execution Console."""

    # Locators
    NAV_EXECUTION_TAB = (By.CSS_SELECTOR, "[data-testid='nav-execution']")
    SUITE_SELECT_ALL = (By.CSS_SELECTOR, "[data-testid='select-suite-all']")
    SUITE_SELECT_API = (By.CSS_SELECTOR, "[data-testid='select-suite-api']")
    SUITE_SELECT_UI = (By.CSS_SELECTOR, "[data-testid='select-suite-ui']")
    BTN_TRIGGER_SUITE = (By.CSS_SELECTOR, "[data-testid='btn-trigger-suite']")
    EXECUTION_STATUS_BADGE = (By.CSS_SELECTOR, "[data-testid='execution-status-badge']")
    EXECUTION_TERMINAL = (By.CSS_SELECTOR, "[data-testid='execution-terminal']")
    EXECUTION_SUMMARY = (By.CSS_SELECTOR, "[data-testid='execution-summary']")

    def navigate_to_execution_tab(self):
        """Navigates to the Execution view via the main navigation bar."""
        logger.info("Switching to Test Execution tab...")
        self.click(*self.NAV_EXECUTION_TAB)
        self.wait_for_visible(*self.BTN_TRIGGER_SUITE)

    def select_suite(self, suite_type: str = "ALL"):
        """Selects test suite radio/button ('ALL', 'API', 'UI')."""
        if suite_type.upper() == "API":
            self.click(*self.SUITE_SELECT_API)
        elif suite_type.upper() == "UI":
            self.click(*self.SUITE_SELECT_UI)
        else:
            self.click(*self.SUITE_SELECT_ALL)

    def run_suite(self):
        """Clicks the suite execution trigger button."""
        logger.info("Clicking suite execution trigger button...")
        self.click(*self.BTN_TRIGGER_SUITE)

    def wait_for_completion(self, timeout: int = 15):
        """Waits for test execution process to complete."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.EXECUTION_STATUS_BADGE).text.strip().upper() in ("COMPLETED", "FAILED", "SUCCESS")
            )
        except Exception:
            self.wait_for_clickable(*self.BTN_TRIGGER_SUITE, timeout=timeout)

    def get_execution_status(self) -> str:
        """Retrieves current execution status text from badge."""
        return self.get_text(*self.EXECUTION_STATUS_BADGE)

    def is_terminal_output_present(self) -> bool:
        """Verifies console log output container is visible and active."""
        return self.is_visible(*self.EXECUTION_TERMINAL)
