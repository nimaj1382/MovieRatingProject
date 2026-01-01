from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.models import Genre, Movie, Director
from .director import DirectorResponse

class MovieBase(BaseModel):
    """Base schema for Movie with shared attributes."""
    id: int = Field(..., description="Unique identifier for the movie")
    title: str = Field(..., max_length=100, description="Movie title (max 100 characters)")
    director: DirectorResponse = Field(..., description="Director of the movie")
    release_year: Optional[int] = Field(None, ge=1888, le=2100, description="Year the movie was released")
    genres: list[str] = Field([], description="List of genre IDs associated with the movie")

class MovieResponse(MovieBase):
    """Schema for Movie response.

    Includes all Movie attributes plus the database-generated id.
    """
    model_config = ConfigDict(from_attributes=True)

    @field_validator('genres', mode='before')
    @classmethod
    def extract_genre_names(cls, v):
        return [genre.name for genre in v]