import os
import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Add project root and backend to python path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "backend" / ".env")

from automation.utils.logger import get_logger
from automation.utils.helpers import capture_failure_screenshot, generate_random_test_payload
from backend.app.database import SessionLocal

logger = get_logger("conftest")

@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Fixture providing base URL for FastAPI backend."""
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

@pytest.fixture(scope="session")
def frontend_base_url() -> str:
    """Fixture providing base URL for React Vite frontend."""
    return os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

@pytest.fixture(scope="function")
def db_session():
    """SQLAlchemy session fixture allowing tests to query and validate database state directly."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def sample_test_case_payload():
    """Provides unique test case payload for API creation testing."""
    return generate_random_test_payload(test_type="API", prefix="APITest")

@pytest.fixture(scope="function")
def driver(request):
    """
    Selenium WebDriver fixture with headless Chrome configuration,
    explicit window sizing, and clean teardown.
    """
    options = Options()
    headless_env = os.getenv("HEADLESS", "true").lower() == "true"
    if headless_env:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    # If Chrome binary path is present in macOS application folder
    mac_chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac_chrome_path):
        options.binary_location = mac_chrome_path

    logger.info("Initializing Selenium Chrome WebDriver...")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        logger.warning(f"Standard Chrome init error: {e}. Retrying without binary override...")
        options.binary_location = ""
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(20)
    driver.implicitly_wait(5)

    yield driver

    logger.info("Tearing down Selenium Chrome WebDriver session...")
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Error closing WebDriver: {e}")

# Pytest hook to capture screenshots on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "driver" in item.funcargs:
            web_driver = item.funcargs["driver"]
            screenshot_path = capture_failure_screenshot(web_driver, item.nodeid)
            logger.error(f"Test '{item.name}' failed. Captured failure screenshot at: {screenshot_path}")
            if hasattr(report, "extra"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra = extra

# Pytest HTML report styling and environment metadata
def pytest_html_report_title(report):
    report.title = "TestPilot - Automated Web & API Testing Platform Report"

def pytest_configure(config):
    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "TestPilot"
        config._metadata["Platform"] = "Automated Web & API Testing Framework"
        config._metadata["SDET Lead"] = "TestPilot Automation Suite"
