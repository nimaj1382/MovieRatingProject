from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from app.db.base import Base


# Association table for many-to-many relationship
movie_genre_association = Table(
    'movie_genre_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)