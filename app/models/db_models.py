from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    full_name = Column(String(100))
    location = Column(String(100))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")
    
    # Add composite index for common queries
    __table_args__ = (
        Index('idx_user_location', 'location'),
        Index('idx_user_created', 'created_at'),
        Index('idx_user_active', 'is_active'),
    )

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    category = Column(String(50), index=True)
    priority = Column(String(20), index=True)
    status = Column(String(20), index=True)
    generated_draft = Column(Text)
    applicable_laws = Column(JSONB)  # Using JSONB for better performance
    suggested_ngos = Column(JSONB)   # Using JSONB for better performance
    next_steps = Column(JSONB)       # Using JSONB for better performance
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="cases")
    feedback = relationship("Feedback", back_populates="case", cascade="all, delete-orphan")
    
    # Add composite indexes for common queries
    __table_args__ = (
        Index('idx_case_user_status', 'user_id', 'status'),
        Index('idx_case_category_status', 'category', 'status'),
        Index('idx_case_created_status', 'created_at', 'status'),
        Index('idx_case_priority', 'priority'),
        # GIN index for JSONB fields for efficient querying
        Index('idx_case_applicable_laws_gin', 'applicable_laws', postgresql_using='gin'),
        Index('idx_case_suggested_ngos_gin', 'suggested_ngos', postgresql_using='gin'),
        Index('idx_case_next_steps_gin', 'next_steps', postgresql_using='gin'),
    )

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.case_id", ondelete="CASCADE"), index=True)
    rating = Column(Integer, index=True)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    case = relationship("Case", back_populates="feedback")
    
    # Add composite index for common queries
    __table_args__ = (
        Index('idx_feedback_case_rating', 'case_id', 'rating'),
        Index('idx_feedback_created', 'created_at'),
    ) 