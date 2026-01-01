from typing import Optional

from app.models import Director
from app.repositories import DirectorRepository
from app.exceptions.service_exception import ExistanceError


class DirectorService:
    """Service layer for Director-related operations."""
    def __init__(self, director_repository: DirectorRepository):
        """Initialize the DirectorService with a DirectorRepository."""
        self.director_repository = director_repository

    def get_director_by_id(self, director_id: int) -> Optional[Director]:
        return self.director_repository.get_by_id(director_id)

    def get_director_by_name(self, name: str) -> Optional[Director]:
        return self.director_repository.get_by_name(name)

    def create_director(self, name: str,
                        birth_year: int = None,
                        description: str = None,
                        ) -> Director:
        # Check if director already exists
        existing_director = self.get_director_by_name(name)
        if existing_director:
            raise ExistanceError(f"Director with name '{name}' already exists.")
        new_director = Director(name=name,
                                birth_year=birth_year,
                                description=description)
        self.director_repository.add(new_director)
        return new_director

