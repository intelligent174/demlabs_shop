from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.pytest_plugin import register_fixture

from app.categories.models import Category
from app.categories.schemas import CategoryCreateRequest


@register_fixture
class CategoryCreateRequestFactory(ModelFactory[CategoryCreateRequest]):
    ...


class CategoryFactory(SQLAlchemyFactory[Category]):
    ...
    # __set_relationships__ = True
