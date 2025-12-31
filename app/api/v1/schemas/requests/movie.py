from typing import Optional
from pydantic import BaseModel, Field

class MovieBase(BaseModel):
    """Base schema for Movie with shared attributes."""
    title: str = Field(..., max_length=100, description="Movie title (max 100 characters)")
    director_id: int = Field(..., description="ID of the movie director")
    release_year: Optional[int] = Field(None, ge=1888, le=2100, description="Year the movie was released")
    genre_ids: Optional[list[int]] = Field(None, description="List of genre IDs associated with the movie")

class MovieCreate(MovieBase):
    """Schema for creating a new movie.

    Validates:
    - title: required, max 100 characters
    - director_id: required
    - release_year: optional, between 1888 and 2100
    - genre_ids: optional list of integers
    """
    pass