from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .associations import movie_genre_association

from app.db.base import Base

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    release_year = Column(DateTime)
    cast = Column(String)
    director_id = Column(
        Integer,
        ForeignKey("directors.id", ondelete="CASCADE"),
        nullable=False
    )

    director = relationship(
        "Director",
        back_populates="movies",
    )