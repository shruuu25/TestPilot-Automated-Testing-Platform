import time
import uuid
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_random_test_payload(test_type: str = "API", prefix: str = "AutoTest") -> Dict[str, Any]:
    """Generates random dynamic test case payload for POST testing."""
    uid = uuid.uuid4().hex[:6]
    return {
        "name": f"{prefix}_{uid}",
        "test_type": test_type,
        "description": f"Automated test case generated during test suite execution #{uid}",
        "endpoint_or_url": f"/api/test/{uid}" if test_type == "API" else f"http://localhost:5173/page/{uid}"
    }

def capture_failure_screenshot(driver, test_name: str) -> str:
    """Saves a PNG screenshot of the current browser state upon test failure."""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        filename = f"{safe_name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        driver.save_screenshot(str(filepath))
        return str(filepath)
    except Exception as e:
        return f"Failed to capture screenshot: {e}"
