from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class CaseBase(BaseModel):
    title: str
    description: str
    category: str
    priority: Optional[str] = "medium"

class CaseCreate(CaseBase):
    pass

class FeedbackCreate(BaseModel):
    case_id: str
    rating: int  # 1-5
    comments: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    rating: int
    comments: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CaseResponse(CaseBase):
    id: int
    case_id: str
    status: str
    generated_draft: Optional[str] = None
    applicable_laws: Optional[List[Dict[str, Any]]] = None
    suggested_ngos: Optional[List[Dict[str, Any]]] = None
    next_steps: Optional[List[str]] = None
    feedback: Optional[List[FeedbackResponse]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class GenerateCaseRequest(BaseModel):
    title: str
    description: str
    category: str
    location: Optional[str] = None

class GenerateCaseResponse(BaseModel):
    case_id: str
    title: str
    category: str
    draft: str
    applicable_laws: List[Dict[str, Any]]
    suggested_ngos: List[Dict[str, Any]]
    next_steps: List[str]
    estimated_timeline: Optional[str] = None
