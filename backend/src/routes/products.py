from fastapi import APIRouter, Depends

from ..schemas.products import (
    BasicProductOut,
    ProductOut
)

from ..services.products import ProductsService


router = APIRouter()


@router.get(
    '/products/{product_id}/basic/',
    response_model=BasicProductOut
)
async def get_basic_product(
    product_id: int,
    products_service: ProductsService = Depends()
):
    await products_service.get_basic_product(
        product_id=product_id
    )


@router.get(
    '/products/{product_id}/',
    response_model=ProductOut
)
async def get_product(
    product_id: int,
    products_service: ProductsService = Depends()
):
    await products_service.get_product(
        product_id=product_id
    )