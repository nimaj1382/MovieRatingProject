from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import SessionLocal
from app.repositories import *
from app.services import *


def get_db() -> Generator:
    """Dependency for getting database session.

    Yields:
        Database session that is automatically closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    """Dependency for getting MovieService.

    Args:
        db: Database session (injected by FastAPI)
    Returns:
        MovieService instance with repository dependencies."""
    if db is None:
        db = next(get_db())
    movie_repo = MovieRepository(db)
    director_repo = DirectorRepository(db)
    return MovieService(movie_repo, director_repo)

def get_director_service(db: Session = Depends(get_db)) -> DirectorService:
    """Dependency for getting DirectorService.

    Args:
        db: Database session (injected by FastAPI)
    Returns:
        DirectorService instance with repository dependencies."""
    if db is None:
        db = next(get_db())
    director_repo = DirectorRepository(db)
    return DirectorService(director_repo)

def get_genre_service(db: Session = Depends(get_db)) -> GenreService:
    """Dependency for getting GenreService.

    Args:
        db: Database session (injected by FastAPI)
    Returns:
        GenreService instance with repository dependencies."""
    if db is None:
        db = next(get_db())
    genre_repo = GenreRepository(db)
    return GenreService(genre_repo)