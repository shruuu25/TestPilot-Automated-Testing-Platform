from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import TestCase
from ..schemas import TestCaseCreate, TestCaseResponse

router = APIRouter(prefix="/api/tests", tags=["Test Cases"])

@router.get("", response_model=List[TestCaseResponse], status_code=status.HTTP_200_OK)
def get_all_tests(
    test_type: Optional[str] = Query(None, description="Filter by 'API' or 'UI'"),
    db: Session = Depends(get_db)
):
    """Retrieve all test definitions, optionally filtered by test_type."""
    query = db.query(TestCase)
    if test_type:
        query = query.filter(TestCase.test_type == test_type.upper())
    return query.order_by(TestCase.id.asc()).all()


@router.get("/{test_id}", response_model=TestCaseResponse, status_code=status.HTTP_200_OK)
def get_test_by_id(test_id: int, db: Session = Depends(get_db)):
    """Retrieve a single test definition by ID."""
    test_case = db.query(TestCase).filter(TestCase.id == test_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test case with id {test_id} not found"
        )
    return test_case


@router.post("", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
def create_test_case(payload: TestCaseCreate, db: Session = Depends(get_db)):
    """Register a new test case definition."""
    new_test = TestCase(
        name=payload.name,
        test_type=payload.test_type,
        description=payload.description,
        endpoint_or_url=payload.endpoint_or_url
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test
