from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from .associations import movie_genre_association

from app.db.base import Base


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)

    movies = relationship(
        "Movie",
        secondary=movie_genre_association,
        back_populates="genres",
    )