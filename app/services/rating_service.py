from typing import Optional

from app.models import Rating, Movie
from app.repositories import RatingRepository, MovieRepository
from app.exceptions.service_exception import ExistanceError


class RatingService:
    """Service layer for Rating-related operations."""
    def __init__(self, rating_repository: RatingRepository,
                 movie_repository: MovieRepository):
        """Initialize the RatingService with repositories."""
        self.rating_repository = rating_repository
        self.movie_repository = movie_repository

    def create_rating(self, movie_id: int, score: float) -> Rating:
        """Create a new rating for a movie.
        
        Args:
            movie_id: ID of the movie to rate
            score: Rating score (1-10)
            
        Returns:
            The created Rating instance
            
        Raises:
            ExistanceError: If movie does not exist
            ValueError: If score is not between 1 and 10
        """
        # Check if movie exists
        movie = self.movie_repository.get_by_id(movie_id)
        if not movie:
            raise ExistanceError(f"Movie with ID '{movie_id}' does not exist.")
        
        # Validate score
        if score < 1 or score > 10:
            raise ValueError("Score must be between 1 and 10.")
        
        # Create rating
        new_rating = Rating(
            movie_id=movie_id,
            score=score
        )
        self.rating_repository.add(new_rating)
        return new_rating

    def get_ratings_for_movie(self, movie_id: int) -> list[Rating]:
        """Get all ratings for a specific movie.
        
        Args:
            movie_id: ID of the movie
            
        Returns:
            List of Rating instances
        """
        return self.rating_repository.get_by_movie_id(movie_id)

    def calculate_average_rating(self, movie_id: int) -> Optional[float]:
        """Calculate the average rating for a movie.
        
        Args:
            movie_id: ID of the movie
            
        Returns:
            Average rating score, or None if no ratings exist
        """
        ratings = self.get_ratings_for_movie(movie_id)
        if not ratings:
            return None
        return sum(r.score for r in ratings) / len(ratings)

    def get_ratings_count(self, movie_id: int) -> int:
        """Get the count of ratings for a movie.
        
        Args:
            movie_id: ID of the movie
            
        Returns:
            Number of ratings
        """
        return len(self.get_ratings_for_movie(movie_id))
