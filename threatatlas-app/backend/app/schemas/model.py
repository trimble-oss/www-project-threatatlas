from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.model import ModelStatus


class ModelBase(BaseModel):
    """Base model schema."""
    name: str
    description: str | None = None


class ModelCreate(ModelBase):
    """Schema for creating a model."""
    diagram_id: int
    framework_id: int


class ModelUpdate(BaseModel):
    """Schema for updating a model."""
    name: str | None = None
    description: str | None = None
    status: ModelStatus | None = None
    completed_at: datetime | None = None


class Model(ModelBase):
    """Schema for model response."""
    id: int
    diagram_id: int
    framework_id: int
    status: ModelStatus
    created_by: int | None
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ModelWithFramework(Model):
    """Schema for model with framework details."""
    framework_name: str
    threat_count: int = 0
    mitigation_count: int = 0

    model_config = ConfigDict(from_attributes=True)
