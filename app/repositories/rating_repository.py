from typing import Optional
from sqlalchemy.orm import Session

from app.models import Rating


class RatingRepository:
    """Repository encapsulating database operations for Rating.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def add(self, rating: Rating) -> None:
        """Persist a new rating.

        Args:
            rating: Rating instance to add.
        """
        self.session.add(rating)
        self.session.commit()

    def get_by_id(self, rating_id: int) -> Optional[Rating]:
        """Fetch a single rating by its primary key.

        Args:
            rating_id: Rating identifier.
        Returns:
            The Rating instance if found; otherwise None.
        """
        return self.session.query(Rating).filter(Rating.id == rating_id).first()

    def get_by_movie_id(self, movie_id: int) -> list[Rating]:
        """Fetch all ratings for a specific movie.

        Args:
            movie_id: Movie identifier.
        Returns:
            List of Rating instances for the movie.
        """
        return self.session.query(Rating).filter(Rating.movie_id == movie_id).all()
