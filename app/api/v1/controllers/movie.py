import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.v1.dependencies import *
from app.api.v1.schemas import *
from app.exceptions import *
from app.services import *
from app.exceptions import *
from app.models import *

router = APIRouter(
    prefix = "/movies",
    tags = ["movies"],
)

# get method for retrieving list of movies which can be all movies or filtered by query parameters (e.g., director_id, genre, release_year)
@router.get(
    "/",
    response_model = ResponseModel,
    summary = "List all movies",
    description = "Retrieve a list of all movies in the system."
)
async def list_movies(
        movie_service: MovieService = Depends(get_movie_service),
        genre_service: GenreService = Depends(get_genre_service),
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        director_name: Optional[str] = None,
        genre: Optional[str] = None,
) -> ResponseModel:
    """List all movies or filter by query parameters.
    Args:
        movie_service: The MovieService dependency.
        genre_service: The GenreService dependency.
        page: Page number for pagination.
        page_size: Number of items per page for pagination.
        title: Optional title to filter movies.
        release_year: Optional release year to filter movies.
        director_name: Optional director name to filter movies.
        genre: Optional genre to filter movies.
    Returns:
        List of movies with their basic information.
    """
    # Check for validation of query parameters if needed
    # In case it's not valid, give an error response with structure of HttpError model

    if not isinstance(page, int) or page < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Page must be a positive integer."
        )
    if not isinstance(page_size, int) or page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Page size must be a positive integer."
        )
    if title is not None and not isinstance(title, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Title must be a string."
        )
    if (release_year is not None and
            (not isinstance(release_year, int)
             or release_year < 1888
             or release_year > 2100)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Release year must be an integer between 1888 and 2100"
        )
    if director_name is not None and not isinstance(director_name, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Director name must be a string."
        )
    if genre is not None and not isinstance(genre, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Genre must be a string."
        )
    if genre:
        genre_obj = genre_service.get_genre_by_name(genre)
        if not genre_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre '{genre}' not found."
            )
        genre = genre_obj

    movies = movie_service.get_movies(
        page=page,
        title=title,
        release_year=release_year,
        director_name=director_name,
        genre=genre,
    )

    movie_responses = [MovieResponse.model_validate(movie) for movie in movies]
    return ResponseModel(
        status="success",
        data={
            "page": page,
            "page_size": page_size,
            "total_items": len(movie_responses),
            "items": movie_responses
        }
    )


@router.get(
    "/{movie_id}",
    response_model = ResponseModel,
    summary = "Get a movie by ID",
    description = "Retrieve a specific movie by its ID."
)
async def get_movie_by_id(
        movie_id: int,
        movie_service: MovieService = Depends(get_movie_service)
) -> ResponseModel:
    """Get a movie by ID.
    Args:
        movie_id: The movie ID
        movie_service: The MovieService dependency.
    Returns:
        The movie with the specified ID.
    Raises:
        HTTPException: 404 if movie not found
    """
    movie = movie_service.get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Movie with id {movie_id} not found"
        )

    movie_response = MovieResponse.model_validate(movie).model_dump()
    return ResponseModel(
        status="success",
        data=movie_response
    )
