from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DirectorBase(BaseModel):
    """Base schema for Director with shared attributes."""
    id: int = Field(..., description="Unique identifier for the director")
    name: str = Field(..., max_length=100, description="Director's name (max 100 characters)")
    birth_year: Optional[int] = Field(None, ge=1800, le=2100, description="Year the director was born")
    description: Optional[str] = Field(None, description="Brief description of the director")

class DirectorResponse(DirectorBase):
    """Schema for Director response.

    Includes all Director attributes plus the database-generated id.
    """
    model_config = ConfigDict(from_attributes=True)