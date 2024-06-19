from dependency_injector import containers
from dependency_injector import providers

from app.carts.repository import CartRepository
from app.categories.repository import CategoryRepository
from app.products.repository import ProductRepository
from app.users.repository import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user_repository = providers.Factory(UserRepository, db_demlabs_shop=gateways.db_demlabs_shop)
    product_repository = providers.Factory(ProductRepository, db_demlabs_shop=gateways.db_demlabs_shop)
    category_repository = providers.Factory(CategoryRepository, db_demlabs_shop=gateways.db_demlabs_shop)
    cart_repository = providers.Factory(CartRepository, db_demlabs_shop=gateways.db_demlabs_shop)
