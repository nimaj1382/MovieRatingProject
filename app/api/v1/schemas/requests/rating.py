from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    """Schema for creating a new rating.

    Validates:
    - score: required, between 1 and 10
    """
    score: float = Field(..., ge=1, le=10, description="Rating score (1-10)")
