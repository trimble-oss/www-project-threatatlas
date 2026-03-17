"""Invitation schemas for API requests and responses."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, ConfigDict


class InvitationCreate(BaseModel):
    """Schema for creating a new invitation."""
    email: EmailStr
    role: Literal['admin', 'standard', 'read_only'] = 'standard'


class InvitationAccept(BaseModel):
    """Schema for accepting an invitation."""
    username: str
    password: str
    full_name: str | None = None


class InvitationResponse(BaseModel):
    """Schema for invitation response."""
    id: int
    email: EmailStr
    role: Literal['admin', 'standard', 'read_only']
    invited_by: int
    is_accepted: bool
    expires_at: datetime
    created_at: datetime
    accepted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class InvitationDetail(InvitationResponse):
    """Schema for detailed invitation with inviter information."""
    inviter_name: str | None = None
    inviter_email: str | None = None
