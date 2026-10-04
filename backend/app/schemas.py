from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

# -----------------
# Health Schemas
# -----------------
class HealthResponse(BaseModel):
    status: str
    database: str
    version: str = "1.0.0"


# -----------------
# TestCase Schemas
# -----------------
class TestCaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the test case")
    test_type: str = Field(..., description="Type of test: 'API' or 'UI'")
    description: Optional[str] = Field(None, description="Detailed explanation of what the test verifies")
    endpoint_or_url: str = Field(..., min_length=1, max_length=500, description="Target API endpoint or web URL")

    @field_validator("test_type")
    @classmethod
    def validate_test_type(cls, v: str) -> str:
        upper_val = v.strip().upper()
        if upper_val not in ("API", "UI"):
            raise ValueError("test_type must be either 'API' or 'UI'")
        return upper_val

    @field_validator("name", "endpoint_or_url")
    @classmethod
    def validate_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseResponse(TestCaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------
# TestResult Schemas
# -----------------
class TestResultBase(BaseModel):
    test_case_id: int
    status: str = Field(..., description="Result outcome: 'PASSED', 'FAILED', or 'SKIPPED'")
    duration: float = Field(0.0, ge=0.0, description="Duration in seconds")
    error_message: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        upper_val = v.strip().upper()
        if upper_val not in ("PASSED", "FAILED", "SKIPPED"):
            raise ValueError("status must be 'PASSED', 'FAILED', or 'SKIPPED'")
        return upper_val


class TestResultCreate(TestResultBase):
    test_run_id: int


class TestResultResponse(TestResultBase):
    id: int
    test_run_id: int
    executed_at: datetime
    test_case_name: Optional[str] = None
    test_type: Optional[str] = None

    class Config:
        from_attributes = True


# -----------------
# TestRun Schemas
# -----------------
class TestRunCreate(BaseModel):
    status: Optional[str] = "RUNNING"
    total_tests: Optional[int] = 0
    passed_tests: Optional[int] = 0
    failed_tests: Optional[int] = 0


class TestRunResponse(BaseModel):
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_tests: int
    passed_tests: int
    failed_tests: int
    status: str

    class Config:
        from_attributes = True


class TestRunDetailResponse(TestRunResponse):
    results: List[TestResultResponse] = []


class RunExecutionRequest(BaseModel):
    test_type: Optional[str] = Field("ALL", description="Filter tests to execute: 'ALL', 'API', or 'UI'")


# -----------------
# Dashboard Stats Schema
# -----------------
class DashboardStatsResponse(BaseModel):
    total_test_cases: int
    total_test_runs: int
    total_passed_tests: int
    total_failed_tests: int
    pass_percentage: float
