from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from automation.utils.logger import get_logger

logger = get_logger("BasePage")

class BasePage:
    """
    Base Page Object providing reusable explicit-wait wrappers,
    safe click/type utilities, and assertions.
    """
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def navigate_to(self, url: str):
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def find_elements(self, by, locator):
        return self.driver.find_elements(by, locator)

    def wait_for_visible(self, by, locator, timeout: int = None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_for_clickable(self, by, locator, timeout: int = None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable((by, locator)))

    def click(self, by, locator):
        element = self.wait_for_clickable(by, locator)
        logger.info(f"Clicking element: {by}={locator}")
        element.click()

    def enter_text(self, by, locator, text: str, clear_first: bool = True):
        element = self.wait_for_visible(by, locator)
        if clear_first:
            element.clear()
        logger.info(f"Entering text into {by}={locator}")
        element.send_keys(text)

    def get_text(self, by, locator) -> str:
        element = self.wait_for_visible(by, locator)
        return element.text.strip()

    def is_visible(self, by, locator, timeout: int = 5) -> bool:
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located((by, locator))).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url
