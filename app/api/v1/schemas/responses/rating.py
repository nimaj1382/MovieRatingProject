from pydantic import BaseModel, Field, ConfigDict


class RatingResponse(BaseModel):
    """Schema for Rating response."""
    id: int = Field(..., description="Unique identifier for the rating")
    movie_id: int = Field(..., description="ID of the movie being rated")
    score: float = Field(..., description="Rating score (1-10)")

    model_config = ConfigDict(from_attributes=True)
