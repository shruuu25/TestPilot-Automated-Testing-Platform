import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .models import TestCase, TestRun, TestResult
from .routes import health, tests, results

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("testpilot.main")

def seed_initial_data(db):
    """Seed baseline test cases and sample run if database is fresh and empty."""
    try:
        count = db.query(TestCase).count()
        if count == 0:
            logger.info("Initializing database with baseline seed test cases...")
            initial_cases = [
                TestCase(name="Verify API Health Endpoint", test_type="API", description="Validates that GET /health returns HTTP 200 with operational status", endpoint_or_url="/health"),
                TestCase(name="Get All Test Cases API", test_type="API", description="Validates that GET /api/tests returns array of registered test definitions", endpoint_or_url="/api/tests"),
                TestCase(name="Create New Test Case API", test_type="API", description="Validates that POST /api/tests creates a valid test record with HTTP 201", endpoint_or_url="/api/tests"),
                TestCase(name="Get Test Case By Valid ID", test_type="API", description="Validates fetching an individual test definition by primary key", endpoint_or_url="/api/tests/{id}"),
                TestCase(name="Negative: Non-existent Test ID", test_type="API", description="Ensures GET /api/tests/999999 gracefully returns HTTP 404", endpoint_or_url="/api/tests/999999"),
                TestCase(name="Negative: Invalid Test Case Payload", test_type="API", description="Ensures POST /api/tests with invalid payload returns HTTP 422", endpoint_or_url="/api/tests"),
                TestCase(name="Dashboard KPI Metrics Render", test_type="UI", description="Verifies total test cases, total runs, and pass rate cards render correctly", endpoint_or_url="http://localhost:5173/"),
                TestCase(name="Test Results Table Render", test_type="UI", description="Verifies that the results table contains columns for Case, Type, Status, Duration", endpoint_or_url="http://localhost:5173/"),
                TestCase(name="Test Execution Trigger", test_type="UI", description="Verifies clicking the Run Tests button triggers suite execution and updates dashboard", endpoint_or_url="http://localhost:5173/"),
                TestCase(name="Status Filter Functionality", test_type="UI", description="Verifies filtering test results table by PASSED and FAILED states", endpoint_or_url="http://localhost:5173/"),
            ]
            db.add_all(initial_cases)
            db.commit()

            # Create an initial completed test run
            sample_run = TestRun(
                started_at=datetime.utcnow() - timedelta(minutes=10),
                completed_at=datetime.utcnow() - timedelta(minutes=9),
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                status="COMPLETED"
            )
            db.add(sample_run)
            db.commit()
            db.refresh(sample_run)

            # Add test results for sample run
            seeded_cases = db.query(TestCase).all()
            for sc in seeded_cases:
                res = TestResult(
                    test_run_id=sample_run.id,
                    test_case_id=sc.id,
                    status="PASSED",
                    duration=0.045 if sc.test_type == "API" else 0.850,
                    error_message=None,
                    executed_at=sample_run.completed_at
                )
                db.add(res)
            db.commit()
            logger.info("Database successfully seeded with initial test definitions and baseline run.")
    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
        db.rollback()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed baseline data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title="TestPilot - Automated Web & API Testing Platform",
    description="Production-style SDET automation & reporting backend API",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to TestPilot API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }

# Register API Routers
app.include_router(health.router)
app.include_router(tests.router)
app.include_router(results.router)
