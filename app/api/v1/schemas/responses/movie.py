from pydantic import BaseModel, Field

from app.models import Genre
from .director import DirectorBase

class MovieBase(BaseModel):
    """Base schema for Movie with shared attributes."""
    id: int = Field(..., description="Unique identifier for the movie")
    title: str = Field(..., max_length=100, description="Movie title (max 100 characters)")
    director: DirectorBase = Field(..., description="Director of the movie")
    release_year: int = Field(..., ge=1888, le=2100, description="Year the movie was released")
    genres: list[str] = Field(..., description="List of genre IDs associated with the movie")

class MovieResponse(MovieBase):
    """Schema for Movie response.

    Includes all Movie attributes plus the database-generated id.
    """
    pass