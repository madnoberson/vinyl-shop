from typing import Optional

from fastapi import APIRouter, Depends

from ..schemas.users import (
    UserOut,
    UserWishlist,
    UserCart
)
from ..services.users import UsersService


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get(
    '/',
    response_model=UserOut
)
async def get_user(
    users_service: UsersService = Depends()
) -> UserOut:
    return await users_service.get_user()


@router.post(
    '/wishlist/',
    status_code=201,
    tags=['wishlist']
)
async def add_to_wishlist(
   product_id: int,
   users_service: UsersService = Depends()
):
    await users_service.add_to_wishlist(
        product_id=product_id
    )


@router.get(
    '/wishlist/',
    response_model=UserWishlist,
    tags=['wishlist']
)
async def get_wishlist(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    users_service: UsersService = Depends()
) -> UserWishlist:
    return await users_service.get_wishlist(
        limit=limit, offset=offset
    )


@router.delete(
    '/wishlist/',
    status_code=204,
    tags=['wishlist']
)
async def delete_from_wishlist(
    product_id: int,
    users_service: UsersService = Depends()
):
    return await users_service.delete_from_wishlist(
        product_id=product_id
    )


@router.post(
    '/cart/',
    status_code=201,
    tags=['cart']
)
async def add_to_cart(
    product_id: int,
    users_service: UsersService = Depends()
):
    await users_service.add_to_cart(
        product_id=product_id
    )


@router.get(
    '/cart/',
    response_model=UserCart,
    tags=['cart']
)
async def get_cart(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    users_service: UsersService = Depends()
):
    return await users_service.get_cart(
        limit=limit, offset=offset
    )


@router.delete(
    '/cart/',
    status_code=204,
    tags=['cart']
)
async def delete_from_cart(
    product_id: int,
    users_service: UsersService = Depends()
):
    await users_service.delete_from_cart(
        product_id=product_id
    )