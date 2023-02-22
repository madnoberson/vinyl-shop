import pytest
from httpx import AsyncClient

from ..services.auth import AuthService


class TestProductsCrud:
    
    @pytest.fixture(scope='class')
    async def token_with_edit_scope(
        fake_user: dict
    ):
        fake_user_data = fake_user | {'scopes': ['edit']}
        token = AuthService.create_token(fake_user_data)

        return token.access_token
        
    @pytest.fixture
    def create_fake_product_input() -> dict:
        return {
            "name": "In the Court of the Crimson King"
        }
    
    @pytest.fixture
    def create_fake_product_output(
        create_fake_product_input: dict
    ) -> dict:
        return create_fake_product_input | {"id": 1}

    @pytest.fixture
    def update_fake_product_input(
        create_fake_product_input: dict
    ):
        return create_fake_product_input | {"name": "Red"}
    
    @pytest.fixture
    def update_fake_product_output(
        update_fake_product_input: dict
    ):
        return update_fake_product_input | {"id": 1}     

    async def test_creating_product_with_no_scope(
        client: AsyncClient,
        create_fake_product_input: dict
    ):
        response = await client.post(
            url='/products/',
            json=create_fake_product_input
        )

        assert response.status_code == 404
    
    async def test_creating_product_with_scope(
        client: AsyncClient,
        create_fake_product_input: dict,
        create_fake_product_output: dict,
        token_with_edit_scope: str
    ):
        response = await client.post(
            url='/products/',
            json=create_fake_product_input,
            headers={
                "Authorization": f"Bearer {token_with_edit_scope}"
            }
        )

        assert response.status_code == 200
        assert response.json() == create_fake_product_output
    
    async def test_updating_product_with_no_scope(
        client: AsyncClient,
        update_fake_product_input: dict
    ):
        fake_product_id = update_fake_product_input.get('id')

        response = await client.patch(
            url=f'/products/{fake_product_id}/',
            json=update_fake_product_input
        )

        assert response.status_code == 404
    
    async def test_updating_product_with_scope(
        client: AsyncClient,
        update_fake_product_input: dict,
        update_fake_product_output: dict,
        token_with_edit_scope: str
    ):
        fake_product_id = update_fake_product_input.get('id')

        response = await client.patch(
            url=f'/products/{fake_product_id}/',
            json=update_fake_product_input,
            headers={
                "Authorization": f"Bearer {token_with_edit_scope}"
            }
        )

        assert response.status_code == 200
        assert response.json() == update_fake_product_output
    
    async def test_deleting_product_with_no_edit_scope(
        client: AsyncClient,
        fake_product: dict
    ):
        product_id = fake_product.get('id')

        response = await client.delete(
            url=f'/products/{product_id}/'
        )

        assert response.status_code == 404
    
    async def test_deleting_product_with_edit_scope(
        client: AsyncClient,
        fake_product: dict,
        token_with_edit_scope: str
    ):
        product_id = fake_product.get('id')

        response = await client.delete(
            url=f'/products/{product_id}/',
            headers={
                "Authorization": f"Bearer {token_with_edit_scope}"
            }
        )

        assert response.status_code == 200
