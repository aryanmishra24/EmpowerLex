from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.db_models import Case
from app.database import get_db

router = APIRouter()

@router.get("/cases/{id}")
def get_case_by_id(id: str, db: Session = Depends(get_db)):
    """Retrieve a specific case by its ID"""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case