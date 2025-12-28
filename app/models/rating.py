from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

from app.db.base import Base

class Rating(Base):
    __tablename__ = 'movie_ratings'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    score = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="ratings")