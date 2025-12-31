from pydantic import BaseModel, Field

class DirectorBase(BaseModel):
    """Base schema for Director with shared attributes."""
    id: int = Field(..., description="Unique identifier for the director")
    name: str = Field(..., max_length=100, description="Director's name (max 100 characters)")
    birth_year: int = Field(..., ge=1800, le=2024, description="Year the director was born")
    description: str = Field(..., description="Brief description of the director")

class DirectorResponse(DirectorBase):
    """Schema for Director response.

    Includes all Director attributes plus the database-generated id.
    """
    pass