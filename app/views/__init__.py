from fastapi import APIRouter

from app.views.registrations import name_prefix as users_name_prefix
from app.views.registrations import router as users_router
from app.views.auth import name_prefix as auth_name_prefix
from app.views.auth import router as auth_router
from app.views.products import name_prefix as product_name_prefix
from app.views.products import router as product_router
from app.views.categories import name_prefix as category_name_prefix
from app.views.categories import router as category_router
from app.views.carts import name_prefix as cart_name_prefix
from app.views.carts import router as cart_router

__all__ = [
    'root_router',
]

root_router = APIRouter()

root_router.include_router(
    router=users_router,
    tags=[users_name_prefix],
    prefix=f'/{users_name_prefix}',
)
root_router.include_router(
    router=auth_router,
    tags=[auth_name_prefix],
    prefix=f'/{auth_name_prefix}'
)
root_router.include_router(
    router=product_router,
    tags=[product_name_prefix],
    prefix=f'/{product_name_prefix}'
)
root_router.include_router(
    router=category_router,
    tags=[category_name_prefix],
    prefix=f'/{category_name_prefix}'
)
root_router.include_router(
    router=cart_router,
    tags=[cart_name_prefix],
    prefix=f'/{cart_name_prefix}'
)
