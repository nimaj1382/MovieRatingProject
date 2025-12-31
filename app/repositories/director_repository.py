from sqlalchemy.orm import Session

from app.models import Director

class DirectorRepository:
    """Repository encapsulating database operations for Director.

    Attributes:
        session: Active SQLAlchemy session used for queries and commits.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session.

        Args:
            session: SQLAlchemy Session instance.
        """
        self.session = session

    def add(self, director: Director) -> None:
        """Persist a new director.

        Args:
            director: Director instance to add.
        """
        self.session.add(director)
        self.session.commit()

    def get_by_id(self, director_id: int) -> Director | None:
        """Fetch a single director by its primary key.

        Args:
            director_id: Director identifier.
        Returns:
            The Director instance if found; otherwise None.
        """
        return self.session.query(Director).filter(Director.id == director_id).first()

    def get_by_name(self, name: str) -> Director | None:
        """Fetch a single director by its name.

        Args:
            name: Director name to match.
        Returns:
            The Director instance if found; otherwise None.
        """
        return self.session.query(Director).filter(Director.name == name).first()