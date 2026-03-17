from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ModelStatus(str, enum.Enum):
    """Status of a threat modeling analysis."""
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"


class Model(Base):
    """
    Represents a threat modeling analysis for a diagram using a specific framework.
    A diagram can have multiple models (e.g., STRIDE analysis, LINDDUN privacy assessment).
    """
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    diagram_id = Column(Integer, ForeignKey("diagrams.id", ondelete="CASCADE"), nullable=False)
    framework_id = Column(Integer, ForeignKey("frameworks.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ModelStatus), default=ModelStatus.in_progress, nullable=False)

    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for migrated data
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    diagram = relationship("Diagram", back_populates="models")
    framework = relationship("Framework")
    creator = relationship("User", foreign_keys=[created_by])
    diagram_threats = relationship("DiagramThreat", back_populates="model", cascade="all, delete-orphan")
    diagram_mitigations = relationship("DiagramMitigation", back_populates="model", cascade="all, delete-orphan")
