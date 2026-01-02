from typing import Optional

from app.models import Rating, Movie
from app.repositories import RatingRepository, MovieRepository
from app.exceptions.service_exception import ExistanceError


class RatingService:
