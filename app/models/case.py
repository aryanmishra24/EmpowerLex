from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    category = Column(String(50), index=True)
    location = Column(String(100))
    status = Column(String(20), default="pending", index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    generated_draft = Column(Text)
    applicable_laws = Column(JSONB)
    suggested_ngos = Column(JSONB)
    next_steps = Column(JSONB)

    # Relationships
    user = relationship("User", back_populates="cases")
    feedback = relationship("Feedback", back_populates="case", cascade="all, delete-orphan")
    
    # Add composite indexes for common queries
    __table_args__ = (
        Index('idx_case_user_status', 'user_id', 'status'),
        Index('idx_case_category_status', 'category', 'status'),
        Index('idx_case_created_status', 'created_at', 'status'),
        # GIN index for JSONB fields for efficient querying
        Index('idx_case_applicable_laws_gin', 'applicable_laws', postgresql_using='gin'),
        Index('idx_case_suggested_ngos_gin', 'suggested_ngos', postgresql_using='gin'),
        Index('idx_case_next_steps_gin', 'next_steps', postgresql_using='gin'),
    ) 