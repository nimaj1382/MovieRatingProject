from sqlalchemy import Column, Integer, String, Table, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .associations import MovieGenreAssociation

from app.db.base import Base


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    birth_year = Column(Integer)

    movies = relationship("Movie", back_populates="director")