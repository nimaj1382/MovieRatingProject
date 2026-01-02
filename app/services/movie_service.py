from typing import Optional, Type, List

from app.models import Movie, Genre
from app.repositories import MovieRepository, DirectorRepository
from app.exceptions.service_exception import *


class MovieService:
    """Service layer for Movie-related operations."""
    def __init__(self, movie_repository: MovieRepository,
                 director_repository: DirectorRepository = None):
        """Initialize the MovieService with a MovieRepository."""
        self.movie_repository = movie_repository
        self.director_repository = director_repository

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
                     cast: str = None,
                     genre: List[Genre] = [],
                     ) -> Movie:
        existing_movie = self.get_movie_by_title(title)
        if existing_movie:
            raise UniquenessError(f"Movie with title '{title}' already exists.")
        director = self.director_repository.get_by_id(director_id)
        if not director:
            raise ExistanceError(f"Director with ID '{director_id}' does not exist.")
        new_movie = Movie(
            title=title,
            director_id=director_id,
            release_year=release_year,
            cast=cast,
        )
        self.movie_repository.add(new_movie)
        for g in genre:
            self.movie_repository.add_genre_to_movie(new_movie, g)
        return new_movie

    def update_movie(self, movie_id: int,
                     title: str = None,
                     director_id: int = None,
                     release_year: int = None,
                     cast: str = None,
                     genres: List[Genre] = None) -> Movie:
        """Update an existing movie.
        
        Args:
            movie_id: ID of the movie to update
            title: New title (optional)
            director_id: New director ID (optional)
            release_year: New release year (optional)
            cast: New cast (optional)
            genres: New list of genres (optional)
            
        Returns:
            Updated Movie instance
            
        Raises:
            ExistanceError: If movie or director does not exist
            UniquenessError: If new title conflicts with existing movie
        """
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            raise ExistanceError(f"Movie with ID '{movie_id}' does not exist.")
        
        # Update title if provided
        if title is not None and title != movie.title:
            existing_movie = self.get_movie_by_title(title)
            if existing_movie:
                raise UniquenessError(f"Movie with title '{title}' already exists.")
            movie.title = title
        
        # Update director if provided
        if director_id is not None:
            director = self.director_repository.get_by_id(director_id)
            if not director:
                raise ExistanceError(f"Director with ID '{director_id}' does not exist.")
            movie.director_id = director_id
        
        # Update other fields if provided
        if release_year is not None:
            movie.release_year = release_year
        if cast is not None:
            movie.cast = cast
        
        # Update genres if provided
        if genres is not None:
            self.movie_repository.update_movie_genres(movie, genres)
        
        self.movie_repository.update(movie)
        return movie

