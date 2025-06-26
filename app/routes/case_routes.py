from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from pydantic import BaseModel
import uuid

from ..models.case_schema import (
    CaseCreate,
    CaseResponse,
    GenerateCaseRequest,
    GenerateCaseResponse,
    FeedbackCreate,
    FeedbackResponse
)
from ..models.user_schema import UserResponse
from app.models.case import Case
from app.models.feedback import Feedback
from ..auth.dependencies import get_current_active_user
from ..database import get_db
from ..agent.legal_agent import LegalAgent
from ..config import settings
from app.agent.tools.ngo_finder import NGOFinderTool

router = APIRouter(prefix="/cases", tags=["cases"])

# Initialize legal agent
legal_agent = LegalAgent(openai_api_key=settings.openai_api_key)

# Initialize NGO finder tool
ngo_finder = NGOFinderTool()

logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

@router.post("/", response_model=CaseResponse)
async def create_case(
    case: CaseCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new legal case"""
    try:
        # Process case through legal agent
        agent_response = await legal_agent.process_case(
            title=case.title,
            description=case.description,
            category=case.category,
            location=current_user.location
        )
        
        # Create case in database
        case_id = uuid.uuid4()
        db_case = Case(
            case_id=case_id,
            title=case.title,
            description=case.description,
            category=case.category,
            status="pending",
            user_id=current_user.id,
            generated_draft=agent_response["draft"],
            applicable_laws=agent_response["applicable_laws"],
            suggested_ngos=agent_response["suggested_ngos"],
            next_steps=agent_response["next_steps"]
        )
        
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        
        return db_case
    except Exception as e:
        logger.error(f"Error creating case: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/generate", response_model=GenerateCaseResponse)
async def generate_case(
    request: GenerateCaseRequest,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Generate case analysis without saving to database"""
    agent_response = await legal_agent.process_case(
        title=request.title,
        description=request.description,
        category=request.category,
        location=request.location or current_user.location
    )
    generated_case_id = uuid.uuid4()
    return GenerateCaseResponse(
        case_id=generated_case_id,
        title=request.title,
        category=request.category,
        draft=agent_response["draft"],
        applicable_laws=agent_response["applicable_laws"],
        suggested_ngos=agent_response["suggested_ngos"],
        next_steps=agent_response["next_steps"]
    )

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: str,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific case by ID"""
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid case ID format"
        )
    
    case = db.query(Case).filter(
        Case.case_id == case_uuid,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Get feedback for the case
    case.feedback = db.query(Feedback).filter(Feedback.case_id == case_uuid).all()
    return case

@router.get("/", response_model=List[CaseResponse])
async def list_cases(
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: Optional[int] = None
):
    """List all cases for the current user"""
    try:
        query = db.query(Case).filter(Case.user_id == current_user.id)
        if limit is not None:
            query = query.offset(skip).limit(limit)
        cases = query.all()
        
        # Get feedback for each case
        for case in cases:
            case.feedback = db.query(Feedback).filter(Feedback.case_id == case.case_id).all()
        
        return cases
    except Exception as e:
        logger.error(f"Error listing cases: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing cases: {str(e)}"
        )

@router.post("/{case_id}/feedback", response_model=FeedbackResponse)
async def create_feedback(
    case_id: str,
    feedback: FeedbackCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create feedback for a case"""
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid case ID format"
        )
    
    # Verify case exists and belongs to user
    case = db.query(Case).filter(
        Case.case_id == case_uuid,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Create feedback
    db_feedback = Feedback(
        case_id=case_uuid,
        rating=feedback.rating,
        comments=feedback.comments
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback

@router.post("/chat")
async def chat_with_agent(
    request: ChatRequest,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Chat with the legal agent"""
    try:
        response = await legal_agent.chat(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing chat request")

@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case_status(
    case_id: str,
    status_update: dict,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update case status"""
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid case ID format"
        )
    
    case = db.query(Case).filter(
        Case.case_id == case_uuid,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Update status
    if "status" in status_update:
        case.status = status_update["status"]
    
    if "priority" in status_update:
        case.priority = status_update["priority"]
    
    db.commit()
    db.refresh(case)
    
    return case

@router.get("/{case_id}/next-steps")
async def get_next_steps(
    case_id: str,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get next steps for a case"""
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid case ID format"
        )
    
    case = db.query(Case).filter(
        Case.case_id == case_uuid,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    return {
        "case_id": str(case.case_id),
        "next_steps": case.next_steps or []
    }

@router.post("/{case_id}/next-steps")
async def update_next_steps(
    case_id: str,
    steps_update: dict,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update next steps for a case"""
    try:
        case_uuid = uuid.UUID(case_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid case ID format"
        )
    
    case = db.query(Case).filter(
        Case.case_id == case_uuid,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    if "next_steps" in steps_update:
        case.next_steps = steps_update["next_steps"]
        db.commit()
        db.refresh(case)
    
    return {
        "case_id": str(case.case_id),
        "next_steps": case.next_steps or []
    }

@router.get("/ngos/search")
async def search_ngos(
    query: str,
    category: Optional[str] = None,
    location: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search for NGOs"""
    try:
        ngos = ngo_finder.search_ngos(query, category, location)
        return {"ngos": ngos}
    except Exception as e:
        logger.error(f"Error searching NGOs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching NGOs")

@router.get("/ngos/category/{category}")
async def get_ngos_by_category(
    category: str,
    location: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get NGOs by category"""
    try:
        ngos = ngo_finder.get_ngos_by_category(category, location)
        return {"ngos": ngos}
    except Exception as e:
        logger.error(f"Error getting NGOs by category: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting NGOs by category")

@router.get("/ngos/location/{location}")
async def get_ngos_by_location(
    location: str,
    category: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get NGOs by location"""
    try:
        ngos = ngo_finder.get_ngos_by_location(location, category)
        return {"ngos": ngos}
    except Exception as e:
        logger.error(f"Error getting NGOs by location: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting NGOs by location") 