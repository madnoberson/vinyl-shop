from fastapi import APIRouter, Depends


from ..schemas.products import (
    BasicProductOut,
    ProductIn,
    ProductOut,
    ProductUpdateIn,
    ProductUpdateOut
)

from ..services.products import ProductsService


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.post(
    '/',
    response_model=ProductOut,
    tags=['admin'],
    status_code=201
)
async def create_product(
    create_product: ProductIn,
    products_service: ProductsService = Depends()
) -> ProductOut:
    return await products_service.create_product(
        create_product=create_product
    )


@router.get(
    '/{product_id}/basic/',
    response_model=BasicProductOut
)
async def get_basic_product(
    product_id: int,
    products_service: ProductsService = Depends()
) -> BasicProductOut:
    return await products_service.get_basic_product(
        product_id=product_id
    )


@router.get(
    '/{product_id}/',
    response_model=ProductOut
)
async def get_product(
    product_id: int,
    products_service: ProductsService = Depends()
) -> ProductOut:
    return await products_service.get_product(
        product_id=product_id
    )


@router.patch(
    '/{product_id}/',
    response_model=ProductUpdateOut,
    tags=['admin']
)
async def update_product(
    product_id: int,
    update_product: ProductUpdateIn,
    products_service: ProductsService = Depends()
) -> ProductUpdateOut:
    return await products_service.update_product(
        product_id=product_id,
        update_product=update_product
    )


@router.delete(
    '/{product_id}/',
    tags=['admin'],
    status_code=204
)
async def delete_product(
    product_id: int,
    products_service: ProductsService = Depends()
):
    await products_service.delete_product(
        product_id=product_id
    )