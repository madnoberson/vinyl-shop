import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_product_with_no_edit_scope(
    client: AsyncClient,
    fake_product: dict
):
    """
        Сценарий: Пользователь с токеном без 'edit scope'
        пытается создать новый товар
    """

    response = await client.post(
        url="/products/",
        json=fake_product
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_product_with_edit_scope(
    client: AsyncClient,
    fake_product: dict,
    shop_employee_token: str
):
    """
        Сценарий: Пользователь с токеном с 'edit scope'
        пытается создать новый товар
    """

    fake_product_out = fake_product.copy()
    fake_product_out['id'] = 1

    response = await client.post(
        url="/products/",
        json=fake_product,
        headers={"Authoraztion": f"Bearer {shop_employee_token}"}
    )

    assert response.status_code == 200
    assert response.json() == fake_product_out