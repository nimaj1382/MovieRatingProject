from typing import Optional, Type, List

from app.models import Movie, Genre
from app.repositories import MovieRepository
from app.exceptions.service_exception import ExistanceError


class MovieService:
    """Service layer for Movie-related operations."""
    def __init__(self, movie_repository: MovieRepository):
        """Initialize the MovieService with a MovieRepository."""
        self.movie_repository = movie_repository

    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        return self.movie_repository.get_by_id(movie_id)

    def get_movie_by_title(self, title: str) -> Optional[Movie]:
        return self.movie_repository.get_by_title(title)

    def get_movies(self, page: int = 1, page_size: int = 10, *,
                    title: Optional[str] = None,
                    release_year: Optional[int] = None,
                    director_name: Optional[str] = None,
                    genre: Optional[Genre] = None
                   ) -> list[Type[Movie]]:
        result_movies = self.movie_repository.find_movies(
            title=title,
            director=director_name,
            release_year=release_year,
            genre=genre,
        )
        return self.paginator(result_movies, page, page_size)

    @staticmethod
    def paginator(input_list: list[Type[Movie]], page: int, page_size: int) -> list[Type[Movie]]:
        """Utility function to paginate a list of items."""
        # Check if page and page_size are valid
        if len(input_list) == 0:
            return []
        if page < 1 or page_size < 1:
            raise ValueError("Page and page_size must be positive integers.")
        max_page = (len(input_list) + page_size - 1) // page_size
        if page > max_page:
            raise ValueError("Page number exceeds maximum number of pages.")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        if start_index >= len(input_list):
            return []
        if end_index >= len(input_list):
            return input_list[start_index:]
        return input_list[start_index:end_index]

    def create_movie(self, title: str,
                     director_id: int,
                     release_year: int = None,
                     genre: List[Genre] = [],
                     ) -> Movie:
        # Check if movie already exists
        existing_movie = self.get_movie_by_title(title)
        if existing_movie:
            raise ExistanceError(f"Movie with title '{title}' already exists.")
        new_movie = Movie(
            title=title,
            director_id=director_id,
            release_year=release_year,
        )
        self.movie_repository.add(new_movie)
        for g in genre:
            self.movie_repository.add_genre_to_movie(new_movie, g)
        return new_movie