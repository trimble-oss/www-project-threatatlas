"""Product collaborator model for sharing products with other users."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from app.database import Base


class ProductCollaborator(Base):
    """Product collaborator model."""

    __tablename__ = "product_collaborators"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(
        ENUM('owner', 'editor', 'viewer', name='collaboratorrole', create_type=False),
        nullable=False,
        default='viewer'
    )
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="collaborators")
    user = relationship("User", foreign_keys=[user_id], back_populates="collaborations")
    added_by_user = relationship("User", foreign_keys=[added_by])

    # Unique constraint: user can only be added once per product
    __table_args__ = (
        UniqueConstraint('product_id', 'user_id', name='unique_product_user'),
    )
