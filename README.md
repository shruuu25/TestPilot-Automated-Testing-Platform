# TESTPILOT – Automated Web & API Testing Platform

> **Production-style, enterprise-grade, interview-ready SDET automation platform uniting REST API testing, Selenium Web UI automation, real-time database telemetry, and interactive React analytics.**

---

## 1. Project Overview

**TestPilot** is an end-to-end SDET test automation platform designed to solve one of the most critical challenges in software quality engineering: **bridging the gap between automated test execution and real-time visibility**.

Instead of running disjointed scripts that output plain text logs into disparate terminal windows, TestPilot combines:
1. **REST API Automation**: High-speed, parameterized API regression testing built with `pytest` and `requests`.
2. **Web UI Automation**: Resilient browser automation with `Selenium WebDriver` employing the **Page Object Model (POM)** and explicit waits.
3. **Database-Backed Test Telemetry**: Relational persistence in MySQL (with zero-config SQLite fallback for local development) recording test case catalogs, execution sessions (`test_runs`), and granular assertions (`test_results`).
4. **Modern React Dashboard**: Single-page application built with React, Vite, and Tailwind CSS showing live KPIs (Pass Rate %, Total Runs, Assertions), filterable execution tables, expandable error traces, and suite execution triggers.
5. **CI/CD Automation Pipeline**: GitHub Actions pipeline providing headless automated regression runs, test reporting, and workflow artifact uploads.

---

## 2. Key Features

- **Centralized Test Repository**: Catalog API and UI test case definitions with metadata (target endpoint, description, type).
- **Execution Telemetry Engine**: Automatic calculation of duration, status (`PASSED`, `FAILED`, `SKIPPED`), and assertion failure traces.
- **Page Object Model (POM)**: Decoupled UI selectors and interaction logic (`BasePage`, `DashboardPage`, `TestExecutionPage`) preventing flaky tests.
- **Automatic Failure Screenshot Capture**: Integrated Pytest hook (`pytest_runtest_makereport`) that snaps full-resolution browser screenshots upon assertion failure into `screenshots/`.
- **Rich HTML Test Reports**: Self-contained HTML test reports generated with `pytest-html`, containing execution metrics, environment metadata, and screenshot attachments.
- **SDET Structured Logging**: Simultaneous dual logging to stdout and `logs/testpilot.log` with timestamps and log levels.
- **RESTful API Backend**: FastAPI service providing auto-generated OpenAPI documentation at `/docs`.
- **Zero-Friction Database Connectivity**: MySQL primary architecture with automated SQLAlchemy fallback to SQLite for immediate local execution.

---

## 3. System Architecture

```mermaid
graph TD
    User([QA Engineer / SDET]) -->|Interacts with UI| React[React + Vite Frontend\n:5173]
    React -->|Axios REST Calls| FastAPI[FastAPI Backend Server\n:8000]
    
    subgraph "Automation Suite (Pytest)"
        PytestRunner[Pytest Test Runner]
        APITests[API Tests: Requests]
        UITests[UI Tests: Selenium POM]
    end

    FastAPI -->|ORM Transactions| DB[(MySQL Database / SQLite)]
    PytestRunner -->|Execute HTTP assertions| FastAPI
    PytestRunner -->|Automate Browser DOM| React
    PytestRunner -->|SQL Assertions & Validation| DB

    PytestRunner -->|Generate| Reports[reports/report.html]
    PytestRunner -->|Log Actions| Logs[logs/testpilot.log]
    PytestRunner -->|Capture Failures| Screenshots[screenshots/*.png]

    GitHubActions[GitHub Actions CI/CD] -->|Run headless on Push/PR| PytestRunner
```

---

## 4. Tech Stack

| Domain | Technologies |
|---|---|
| **Backend API** | Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, PyMySQL, Pydantic v2 |
| **Test Automation** | Pytest, Selenium WebDriver (Chrome Headless), Requests, pytest-html, pytest-rerunfailures |
| **Frontend Dashboard** | React 18, Vite, Tailwind CSS, Lucide Icons, Axios |
| **Database** | MySQL 8.0+ (with SQLite fallback support) |
| **CI / CD** | GitHub Actions (`ubuntu-latest`, MySQL Service Container, Headless Chrome) |
| **Source Control** | Git, GitHub |

---

## 5. Folder Structure

```
TestPilot/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app setup, CORS, lifespan seeding
│   │   ├── database.py          # SQLAlchemy engine & session factory
│   │   ├── models.py            # TestCase, TestRun, TestResult ORM models
│   │   ├── schemas.py           # Pydantic v2 schemas and validation
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── tests.py         # /api/tests endpoints
│   │       ├── results.py       # /api/results, /api/runs, /api/stats
│   │       └── health.py        # /health endpoint
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── automation/
│   ├── tests/
│   │   ├── api/
│   │   │   ├── test_health.py       # Health check & root API tests
│   │   │   ├── test_tests_api.py    # Test case CRUD & negative validations
│   │   │   └── test_results_api.py  # Run triggers & stats validations
│   │   │
│   │   └── ui/
│   │       ├── test_dashboard.py       # Dashboard KPIs & table checks
│   │       └── test_test_execution.py  # Suite execution triggers
│   │
│   ├── pages/
│   │   ├── base_page.py            # Generic POM explicit wait wrappers
│   │   ├── dashboard_page.py       # Dashboard locators and actions
│   │   └── test_execution_page.py  # Execution console POM
│   │
│   ├── utils/
│   │   ├── logger.py               # SDET dual console/file logging
│   │   └── helpers.py              # Random data generators & screenshot helper
│   │
│   ├── conftest.py                 # Pytest fixtures & makereport screenshot hook
│   ├── pytest.ini                  # Pytest configuration & markers
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── KPICard.jsx
│   │   │   ├── TestResultsTable.jsx
│   │   │   ├── RecentRunsTable.jsx
│   │   │   └── NewTestCaseModal.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   └── TestExecutionPage.jsx
│   │   ├── services/
│   │   │   └── api.js              # Centralized Axios client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── database/
│   ├── schema.sql                  # MySQL DDL table creation script
│   └── seed.sql                    # Initial seed data for test cases & runs
│
├── reports/
│   └── .gitkeep                    # Stores generated HTML test reports
│
├── screenshots/
│   └── .gitkeep                    # Stores failure screenshots (.png)
│
├── logs/
│   └── .gitkeep                    # Stores runtime test logs (testpilot.log)
│
├── .github/
│   └── workflows/
│       └── tests.yml               # GitHub Actions CI workflow
│
├── .gitignore
├── README.md
└── .env.example
```

---

## 6. Prerequisites

- **Python**: Version 3.11 or newer
- **Node.js**: Version 18 or 20+
- **Google Chrome**: Installed (for Selenium UI tests)
- **MySQL Server** (Optional for local dev; SQLite fallback is built-in): MySQL 8.0+

---

## 7. Installation & Setup

### 7.1 Clone and Setup Virtual Environment
```bash
git clone https://github.com/your-username/TestPilot.git
cd TestPilot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python backend and automation dependencies
pip install -r backend/requirements.txt -r automation/requirements.txt
```

### 7.2 Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default configuration:
```env
# MySQL Database URL:
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/testpilot

# Or use SQLite for local zero-dependency development:
# DATABASE_URL=sqlite:///./testpilot.db

API_BASE_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:5173
HEADLESS=true
```

### 7.3 MySQL Database Setup (Optional)
If using MySQL locally:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p testpilot < database/seed.sql
```
*(If MySQL is not installed locally, TestPilot automatically utilizes SQLite `testpilot.db` and auto-seeds baseline data seamlessly on startup).*

### 7.4 Frontend Installation
```bash
cd frontend
npm install
cd ..
```

---

## 8. Running the Application

### Start Backend API
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Root: `http://127.0.0.1:8000/`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/health`

### Start Frontend Dashboard
In a separate terminal:
```bash
cd frontend
npm run dev
```
- Open Browser: `http://localhost:5173`

---

## 9. Running Automated Tests

Make sure the backend and frontend are running, then run tests from the project root:

### Run Full Test Suite
```bash
pytest automation/tests -v
```

### Run Only REST API Tests
```bash
pytest automation/tests -m api -v
```

### Run Only Web UI Automation Tests
```bash
pytest automation/tests -m ui -v
```

### Run Smoke Tests
```bash
pytest automation/tests -m smoke -v
```

### Generate Standalone HTML Report
```bash
pytest automation/tests -v --html=reports/report.html --self-contained-html
```
Open `reports/report.html` in your browser to view full test execution metrics, test durations, and embedded failure screenshots.

---

## 10. SDET Design Patterns & Core Concepts

### Page Object Model (POM)
- UI interactions and locators are encapsulated in `automation/pages/`.
- Test scripts (`test_dashboard.py`, `test_test_execution.py`) remain clean, readable, and decoupled from HTML DOM changes.
- `BasePage` encapsulates explicit wait logic (`WebDriverWait` and `expected_conditions`), eliminating flaky `time.sleep()` calls.

### Parameterized Testing
- Pytest `@pytest.mark.parametrize` is utilized in `test_tests_api.py` to test boundary conditions, malformed payloads, and missing fields in a single clean test method.

### Direct Database Validation
- In `test_create_test_case_success`, after asserting the HTTP response code (201 Created), the test uses the `db_session` fixture to query the database table directly, verifying data persistence integrity.

### Automatic Failure Screenshots
- Pytest's `pytest_runtest_makereport` hook in `conftest.py` monitors execution outcomes. Upon any UI test failure, it captures a PNG screenshot into `screenshots/` and embeds it directly into the HTML test report.

---

## 11. CI/CD with GitHub Actions

The repository includes a production-grade CI pipeline in `.github/workflows/tests.yml`:
- **Triggers**: On every `push` and `pull_request` to `main`.
- **Database Service Container**: Spins up a real MySQL 8.0 instance with health check verification.
- **Headless Execution**: Runs headless Google Chrome on Ubuntu runner.
- **Reporting Artifacts**: Collects `reports/report.html`, `screenshots/`, and `logs/testpilot.log` and publishes them via `actions/upload-artifact@v4`.

---

## 12. Interview Talking Points (How to Explain TestPilot)

> *"In TestPilot, I engineered an end-to-end SDET test automation platform that bridges test execution with test observability.*
>
> *On the backend, I built a high-performance FastAPI service backed by SQLAlchemy and MySQL that exposes endpoints for test catalogs, execution runs, and real-time KPIs.*
>
> *For automation, I implemented a robust Pytest framework combining Requests for API automation and Selenium WebDriver with the Page Object Model for UI validation. I utilized custom Pytest fixtures for environment injection and direct database validation, explicit waits for DOM synchronization, and a custom `pytest_runtest_makereport` hook that automatically captures failure screenshots and embeds them into self-contained HTML reports.*
>
> *On the frontend, I developed a responsive React dashboard with Vite and Tailwind CSS that allows QA engineers to monitor test metrics, filter historical results, inspect failure stack traces, and trigger targeted test suite executions.*
>
> *Finally, I automated the entire test lifecycle using GitHub Actions with a MySQL service container and automated artifact publishing."*

---

## 13. Future Improvements

- Add WebSocket support for live streaming test execution progress line-by-line.
- Integrate Slack/Teams webhook notifications on suite failure.
- Add support for test execution scheduling (cron-based automated nightly runs).
