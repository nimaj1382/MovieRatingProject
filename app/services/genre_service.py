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

    def genre_names_to_genre_list(self, genre_names: list[str]) -> list[Genre]:
        """Convert a list of genre names to a list of Genre objects."""
        genres = []
        for name in genre_names:
            genre = self.get_genre_by_name(name)
            if genre:
                genres.append(genre)
            else:
                raise ExistanceError(f"Genre with name '{name}' does not exist.")
        return genres

    def genre_ids_to_genre_list(self, genre_ids: list[int]) -> list[Genre]:
        """Convert a list of genre IDs to a list of Genre objects."""
        genres = []
        for genre_id in genre_ids:
            genre = self.get_genre_by_id(genre_id)
            if genre:
                genres.append(genre)
            else:
                raise ExistanceError(f"Genre with ID '{genre_id}' does not exist.")
        return genres

    @staticmethod
    def genre_list_to_genre_names(genres: list[Genre]) -> list[str]:
        """Convert a list of Genre objects to a list of genre names."""
        return [genre.name for genre in genres]