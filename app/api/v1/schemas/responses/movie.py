from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from app.models import Genre, Movie, Director
from .director import DirectorResponse

class MovieBase(BaseModel):
    """Base schema for Movie with shared attributes."""
    id: int = Field(..., description="Unique identifier for the movie")
    title: str = Field(..., max_length=100, description="Movie title (max 100 characters)")
    director: DirectorResponse = Field(..., description="Director of the movie")
    release_year: Optional[int] = Field(None, ge=1888, le=2100, description="Year the movie was released")
    cast: Optional[str] = Field(None, description="Cast of the movie")
    genres: list[str] = Field([], description="List of genre names associated with the movie")
    average_rating: Optional[float] = Field(None, description="Average rating score")
    ratings_count: int = Field(0, description="Number of ratings")

class MovieResponse(MovieBase):
    """Schema for Movie response.

    Includes all Movie attributes plus the database-generated id.
    """
    model_config = ConfigDict(from_attributes=True)

    @field_validator('genres', mode='before')
    @classmethod
    def extract_genre_names(cls, v):
        return [genre.name for genre in v]

    @model_validator(mode='before')
    @classmethod
    def compute_ratings(cls, data):
        """Calculate average rating and count from ratings relationship."""
        if hasattr(data, 'ratings'):
            ratings = data.ratings
            if ratings:
                data.average_rating = round(sum(r.score for r in ratings) / len(ratings), 1)
                data.ratings_count = len(ratings)
            else:
                data.average_rating = None
                data.ratings_count = 0
        return data
