"""Schemas for product collaboration."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class CollaboratorAdd(BaseModel):
    """Schema for adding a collaborator to a product."""
    user_id: int
    role: Literal['owner', 'editor', 'viewer'] = 'viewer'


class CollaboratorUpdate(BaseModel):
    """Schema for updating a collaborator's role."""
    role: Literal['owner', 'editor', 'viewer']


class CollaboratorResponse(BaseModel):
    """Schema for collaborator response."""
    id: int
    product_id: int
    user_id: int
    role: Literal['owner', 'editor', 'viewer']
    added_by: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollaboratorWithDetails(CollaboratorResponse):
    """Schema for collaborator with user details."""
    user_email: str
    user_username: str
    user_full_name: str | None
    added_by_username: str
