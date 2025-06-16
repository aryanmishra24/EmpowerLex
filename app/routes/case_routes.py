from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from pydantic import BaseModel
import json
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
        
        # Ensure next_steps is properly awaited and serializable
        next_steps = agent_response.get("next_steps", [])
        if isinstance(next_steps, list):
            next_steps_json = json.dumps(next_steps)
        else:
            next_steps_json = json.dumps([str(next_steps)])
        
        # Create case in database
        case_id = str(uuid.uuid4())
        db_case = Case(
            case_id=case_id,
            title=case.title,
            description=case.description,
            category=case.category,
            status="pending",
            user_id=current_user.id,
            generated_draft=agent_response["draft"],
            applicable_laws=json.dumps(agent_response["applicable_laws"]),
            suggested_ngos=json.dumps(agent_response["suggested_ngos"]),
            next_steps=next_steps_json
        )
        
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        
        # Deserialize JSON fields for response
        db_case.applicable_laws = json.loads(db_case.applicable_laws) if db_case.applicable_laws else []
        db_case.suggested_ngos = json.loads(db_case.suggested_ngos) if db_case.suggested_ngos else []
        db_case.next_steps = json.loads(db_case.next_steps) if db_case.next_steps else []
        
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
    generated_case_id = str(uuid.uuid4())
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
    case = db.query(Case).filter(
        Case.case_id == case_id,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    # Ensure case_id is set
    if not case.case_id:
        case.case_id = str(uuid.uuid4())
        db.commit()
    # Deserialize JSON fields
    case.applicable_laws = json.loads(case.applicable_laws) if case.applicable_laws else []
    case.suggested_ngos = json.loads(case.suggested_ngos) if case.suggested_ngos else []
    case.next_steps = json.loads(case.next_steps) if case.next_steps else []
    # Get feedback for the case
    case.feedback = db.query(Feedback).filter(Feedback.case_id == case_id).all()
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
        
        # Deserialize JSON fields for each case
        for case in cases:
            # Ensure case_id is set
            if not case.case_id:
                case.case_id = str(uuid.uuid4())
                db.commit()
            
            # Deserialize JSON fields
            case.applicable_laws = json.loads(case.applicable_laws) if case.applicable_laws else []
            case.suggested_ngos = json.loads(case.suggested_ngos) if case.suggested_ngos else []
            
            # Handle next_steps - ensure it's a list of strings
            if case.next_steps:
                try:
                    next_steps = json.loads(case.next_steps)
                    if isinstance(next_steps, list):
                        # If it's a list of objects, extract the step and actions
                        formatted_steps = []
                        for step in next_steps:
                            if isinstance(step, dict):
                                if 'step' in step:
                                    formatted_steps.append(step['step'])
                                if 'actions' in step and isinstance(step['actions'], list):
                                    formatted_steps.extend(step['actions'])
                            elif isinstance(step, str):
                                formatted_steps.append(step)
                        case.next_steps = formatted_steps
                    else:
                        case.next_steps = []
                except json.JSONDecodeError:
                    case.next_steps = []
            else:
                case.next_steps = []
        
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
    case = db.query(Case).filter(
        Case.case_id == case_id,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    db_feedback = Feedback(
        user_id=current_user.id,
        case_id=case_id,
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
    response = await legal_agent.chat(request.message)
    return {"response": response} 

@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case_status(
    case_id: str,
    status_update: dict,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update case status"""
    case = db.query(Case).filter(
        Case.case_id == case_id,
        Case.user_id == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Update status
    case.status = status_update.get("status", case.status)
    db.commit()
    db.refresh(case)
    
    # Deserialize JSON fields
    case.applicable_laws = json.loads(case.applicable_laws) if case.applicable_laws else []
    case.suggested_ngos = json.loads(case.suggested_ngos) if case.suggested_ngos else []
    case.next_steps = json.loads(case.next_steps) if case.next_steps else []
    
    return case

# Next steps endpoints
@router.get("/{case_id}/next-steps")
async def get_next_steps(
    case_id: str,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get next steps for a case"""
    try:
        case = db.query(Case).filter(
            Case.case_id == case_id,
            Case.user_id == current_user.id
        ).first()
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Handle None or empty next_steps
        if not case.next_steps:
            return {"steps": []}
        
        try:
            next_steps = json.loads(case.next_steps)
            if not isinstance(next_steps, list):
                next_steps = []
            return {"steps": next_steps}
        except json.JSONDecodeError:
            logger.error(f"Error decoding next steps for case {case_id}")
            return {"steps": []}
            
    except Exception as e:
        logger.error(f"Error getting next steps: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting next steps: {str(e)}"
        )

@router.post("/{case_id}/next-steps")
async def update_next_steps(
    case_id: str,
    steps_update: dict,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update next steps for a case"""
    try:
        case = db.query(Case).filter(
            Case.case_id == case_id,
            Case.user_id == current_user.id
        ).first()
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Validate steps
        steps = steps_update.get("steps", [])
        if not isinstance(steps, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Steps must be a list"
            )
        
        # Update next steps
        case.next_steps = json.dumps(steps)
        db.commit()
        db.refresh(case)
        
        # Return updated steps
        try:
            return {"steps": json.loads(case.next_steps)}
        except json.JSONDecodeError:
            return {"steps": []}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating next steps: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating next steps: {str(e)}"
        )

# NGO finder endpoints
@router.get("/ngos/search")
async def search_ngos(
    query: str,
    category: Optional[str] = None,
    location: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search NGOs by query, category, and/or location"""
    # Get all NGOs from the mock database
    all_ngos = []
    
    # Map frontend categories to backend categories
    category_mapping = {
        "Legal Aid": ["consumer protection", "labour law", "family law", "criminal law", "property law"],
        "Women Rights": ["family law"],
        "Child Rights": ["family law"],
        "Human Rights": ["criminal law"]
    }
    
    # Map frontend locations to backend locations
    location_mapping = {
        "Delhi": ["New Delhi", "Delhi"],
        "Mumbai": ["Mumbai"],
        "Bangalore": ["Bangalore"],
        "Chennai": ["Chennai"],
        "Kolkata": ["Kolkata"]
    }
    
    # If category is specified, get NGOs from mapped categories
    if category and category != "All":
        categories = category_mapping.get(category, [])
        for cat in categories:
            ngos = ngo_finder._run(cat)
            all_ngos.extend(ngos)
    else:
        # Get NGOs from all categories
        for cat in ["consumer protection", "labour law", "family law", "criminal law", "property law"]:
            ngos = ngo_finder._run(cat)
            all_ngos.extend(ngos)
    
    # Filter NGOs by query and location
    filtered_ngos = []
    for ngo in all_ngos:
        matches_query = not query or (
            query.lower() in ngo['name'].lower() or 
            any(query.lower() in service.lower() for service in ngo['services'])
        )
        
        # Check location match
        matches_location = True
        if location and location != "All":
            location_keywords = location_mapping.get(location, [location])
            matches_location = any(
                keyword.lower() in ngo['address'].lower() 
                for keyword in location_keywords
            )
        
        if matches_query and matches_location:
            filtered_ngos.append(ngo)
    
    return filtered_ngos

@router.get("/ngos/category/{category}")
async def get_ngos_by_category(
    category: str,
    location: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get NGOs by category and optionally by location"""
    # Map frontend categories to backend categories
    category_mapping = {
        "Legal Aid": ["consumer protection", "labour law", "family law", "criminal law", "property law"],
        "Women Rights": ["family law"],
        "Child Rights": ["family law"],
        "Human Rights": ["criminal law"]
    }
    
    # Map frontend locations to backend locations
    location_mapping = {
        "Delhi": ["New Delhi", "Delhi"],
        "Mumbai": ["Mumbai"],
        "Bangalore": ["Bangalore"],
        "Chennai": ["Chennai"],
        "Kolkata": ["Kolkata"]
    }
    
    # Get NGOs for the specified category
    categories = category_mapping.get(category, [])
    
    all_ngos = []
    for cat in categories:
        ngos = ngo_finder._run(cat)
        all_ngos.extend(ngos)
    
    # Filter by location if specified
    if location and location != "All":
        location_keywords = location_mapping.get(location, [location])
        all_ngos = [
            ngo for ngo in all_ngos 
            if any(keyword.lower() in ngo['address'].lower() for keyword in location_keywords)
        ]
    
    return all_ngos

@router.get("/ngos/location/{location}")
async def get_ngos_by_location(
    location: str,
    category: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get NGOs by location and optionally by category"""
    # Get all NGOs from the mock database
    all_ngos = []
    
    # Map frontend categories to backend categories
    category_mapping = {
        "Legal Aid": ["consumer protection", "labour law", "family law", "criminal law", "property law"],
        "Women Rights": ["family law"],
        "Child Rights": ["family law"],
        "Human Rights": ["criminal law"]
    }
    
    # Map frontend locations to backend locations
    location_mapping = {
        "Delhi": ["New Delhi", "Delhi"],
        "Mumbai": ["Mumbai"],
        "Bangalore": ["Bangalore"],
        "Chennai": ["Chennai"],
        "Kolkata": ["Kolkata"]
    }
    
    # If category is specified, get NGOs from mapped categories
    if category and category != "All":
        categories = category_mapping.get(category, [])
        for cat in categories:
            ngos = ngo_finder._run(cat)
            all_ngos.extend(ngos)
    else:
        # Get NGOs from all categories
        for cat in ["consumer protection", "labour law", "family law", "criminal law", "property law"]:
            ngos = ngo_finder._run(cat)
            all_ngos.extend(ngos)
    
    # Filter NGOs by location
    location_keywords = location_mapping.get(location, [location])
    filtered_ngos = [
        ngo for ngo in all_ngos 
        if any(keyword.lower() in ngo['address'].lower() for keyword in location_keywords)
    ]
    return filtered_ngos 