from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FrameworkBase(BaseModel):
    """Base schema for Framework."""
    name: str
    description: str | None = None


class FrameworkCreate(FrameworkBase):
    """Schema for creating a Framework."""
    pass


class FrameworkUpdate(FrameworkBase):
    """Schema for updating a Framework."""
    name: str | None = None


class Framework(FrameworkBase):
    """Schema for Framework response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
