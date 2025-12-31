from typing import Optional

from app.models import Genre
from app.repositories import GenreRepository
from app.exceptions.service_exception import ExistanceError


class GenreService:
    """Service layer for Genre-related operations."""
    def __init__(self, genre_repository: GenreRepository):
        """Initialize the GenreService with a GenreRepository."""
        self.genre_repository = genre_repository

    def get_genre_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.genre_repository.get_by_id(genre_id)

    def get_genre_by_name(self, name: str) -> Optional[Genre]:
        return self.genre_repository.get_by_name(name)

    def create_genre(self, name: str, description: str = None) -> Genre:
        # Check if genre already exists
        existing_genre = self.get_genre_by_name(name)
        if existing_genre:
            raise ExistanceError(f"Genre with name '{name}' already exists.")
        new_genre = Genre(name=name, description=description)
        self.genre_repository.add(new_genre)
        return new_genre