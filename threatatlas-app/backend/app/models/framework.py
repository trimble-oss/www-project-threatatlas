from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Framework(Base):
    """Threat modeling framework (e.g., STRIDE, PASTA)."""

    __tablename__ = "frameworks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    threats = relationship("Threat", back_populates="framework", cascade="all, delete-orphan")
    mitigations = relationship("Mitigation", back_populates="framework", cascade="all, delete-orphan")
