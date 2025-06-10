from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    location = Column(String)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    generated_draft = Column(Text)
    applicable_laws = Column(JSON)
    suggested_ngos = Column(JSON)
    next_steps = Column(JSON)

    # Relationships
    user = relationship("User", back_populates="cases")
    feedback = relationship("Feedback", back_populates="case", cascade="all, delete-orphan") 