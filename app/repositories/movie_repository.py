from typing import Optional, Type

from sqlalchemy.orm import Session

from app.models import Movie, Genre, Director

class MovieRepository:
    """Repository encapsulating database operations for Movie.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def add(self, movie: Movie) -> None:
        """Persist a new movie.

        Args:
            movie: Movie instance to add.
        """
        self.session.add(movie)
        self.session.commit()

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Fetch a single movie by its primary key.

        Args:
            movie_id: Movie identifier.
        Returns:
            The Movie instance if found; otherwise None.
        """
        return self.session.query(Movie).filter(Movie.id == movie_id).first()

    def get_by_title(self, title: str) -> Optional[Movie]:
        """Fetch a single movie by its title.

        Args:
            title: Movie title to match.
        Returns:
            The Movie instance if found; otherwise None.
        """
        return self.session.query(Movie).filter(Movie.title == title).first()

    def find_movies(self, *,
                    title: str = None,
                    director: str = None,
                    release_year: int = None,
                    genre: Genre = None) -> list[Type[Movie]]:
        """Find movies matching given criteria.

        Args:
            title: Title to filter by (optional).
            director: Director to filter by (optional).
            release_year: Release year to filter by (optional).
            genre: Genre to filter by (optional).
        Returns:
            List of Movie instances matching criteria.
        """
        query = self.session.query(Movie)
        query = query.join(Movie.director)
        query = query.join(Movie.genres)
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if director:
            query = query.filter(Director.name.ilike(f"%{director}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre:
            query = query.filter(Genre.name == genre)
        return query.all()
