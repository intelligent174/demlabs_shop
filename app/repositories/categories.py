from app.core.repository.base import BaseAlchemyRepository
from app.models.categories import Category
from app.schemas.responses.categories import CategoryCreateResponse

__all__ = [
    'CategoryRepository',
]


class CategoryRepository(BaseAlchemyRepository):
    model = Category
    creation_schema = CategoryCreateResponse
