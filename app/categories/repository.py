from app.core.repository.base import BaseAlchemyRepository
from app.categories.models import Category
from app.categories.schemas import CategoryCreateResponse

__all__ = [
    'CategoryRepository',
]


class CategoryRepository(BaseAlchemyRepository):
    model = Category
    creation_schema = CategoryCreateResponse
