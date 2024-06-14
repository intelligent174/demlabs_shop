from app.core.service.base import BaseCreateService
from app.resources.categories import CATEGORY_NOT_FOUND, CATEGORY_ALREADY_EXISTS

__all__ = [
    'CategoryService',
]


class CategoryService(BaseCreateService):
    _errors_map = {
        'NoResultFound': CATEGORY_NOT_FOUND,
        'category_title_key': CATEGORY_ALREADY_EXISTS,
    }
