from app.core.cache.base import BaseRedisService

__all__ = [
    'ProductRedisService',
]

from app.products.schemas import ProductCreateResponse


class ProductRedisService(BaseRedisService[ProductCreateResponse]):
    __service_key__ = 'product'

    getion_schema = ProductCreateResponse
