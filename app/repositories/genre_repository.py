from sqlalchemy.orm import Session

from app.models import Genre

class GenreRepository:
    """Repository encapsulating database operations for Genre.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def add(self, genre: Genre) -> None:
        """Persist a new genre.

        Args:
            genre: Genre instance to add.
        """
        self.session.add(genre)
        self.session.commit()

    def get_by_id(self, genre_id: int) -> Genre | None:
        """Fetch a single genre by its primary key.

        Args:
            genre_id: Genre identifier.
        Returns:
            The Genre instance if found; otherwise None.
        """
        return self.session.query(Genre).filter(Genre.id == genre_id).first()

    def get_by_name(self, name: str) -> Genre | None:
        """Fetch a single genre by its name.

        Args:
            name: Genre name to match.
        Returns:
            The Genre instance if found; otherwise None.
        """
        return self.session.query(Genre).filter(Genre.name == name).first()