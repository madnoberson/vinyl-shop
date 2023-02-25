from datetime import datetime

import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient


@pytest.fixture
def create_fake_product_input() -> dict:
    return {
        "name": "In the Court of the Crimson King"
    }


@pytest.fixture
def create_fake_product_output() -> dict:
    return {
        "product": {
            "id": 1,
            "name": "In the Court of the Crimson King"
        },
        "updates": None
    }


@pytest.fixture
def update_fake_product_input():
    return {
        "name": "Red",
        "description": "Изменил название альбома"
    }


@pytest.fixture
def update_fake_product_output():
    return {
        "product": {
            "id": 1,
            "name": "Red"
        },
        "update": {
            "created_by": 2,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Изменил название альбома"
        }
    }


@pytest.mark.anyio
class TestProductsCrud:

    @pytest.mark.parametrize(
        [
            "input",
            "expected_status_code",
            "expected_output",
            "token"
        ],
        [
            (
                lazy_fixture("create_fake_product_input"),
                201,
                lazy_fixture("create_fake_product_output"),
                lazy_fixture("token_with_edit_scope")
            ),
            (
                lazy_fixture("create_fake_product_input"),
                403,
                None,
                None
            ),
            (
                lazy_fixture("create_fake_product_input"),
                403,
                None,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                {"data": "some invalid data"},
                422,
                None,
                lazy_fixture("token_with_edit_scope")
            )
        ]
    )
    async def test_creating_poduct(
        self,
        client: AsyncClient,
        input: dict,
        expected_status_code: int,
        expected_output: dict | None,
        token: str | None
    ):
        headers = None
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }

        response = await client.post(
                url='/products/',
                json=input,
                headers=headers
            )
        
        assert response.status_code == expected_status_code

        if expected_output:
            assert response.json() == expected_output

    @pytest.mark.parametrize(
        [
            "fake_product_id",
            "input",
            "expected_status_code",
            "expected_output",
            "token"
        ],
        [
            (
               1,
               lazy_fixture("update_fake_product_input"),
               200,
               lazy_fixture("update_fake_product_output"),
               lazy_fixture("token_with_edit_scope") 
            ),
            (
                -1,
                lazy_fixture("update_fake_product_input"),
                404,
                None,
                lazy_fixture("token_with_edit_scope")
            ),
            (
                'first',
                lazy_fixture("update_fake_product_input"),
                422,
                None,
                lazy_fixture("token_with_edit_scope")
            ),
            (
                1,
                lazy_fixture("update_fake_product_input"),
                403,
                None,
                None
            ),
            (
                1,
                lazy_fixture("update_fake_product_input"),
                403,
                None,
                lazy_fixture("token_with_no_scopes")
            ),
            (
               1,
               {"data": "some invalid data"},
               422,
               None,
               lazy_fixture("token_with_edit_scope") 
            )
        ]
    )
    async def test_updating_product(
        self,
        client: AsyncClient,
        fake_product_id: int,
        input: dict,
        expected_status_code: int,
        expected_output: dict | None,
        token: str | None
    ):
        headers = None
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
        
        response = await client.patch(
            url=f'/products/{fake_product_id}/',
            json=input,
            headers=headers
        )

        assert response.status_code == expected_status_code

        if expected_output:
            assert response.json() == expected_output
    
    @pytest.mark.parametrize(
        [   
            "fake_product_id",
            "expected_status_code",
            "token"
        ],
        [
            (
                1,
                403,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                1,
                403,
                None
            ),
            (
                1,
                204,
                lazy_fixture("token_with_edit_scope")
            ),
            (
               -1,
               404,
               lazy_fixture("token_with_edit_scope")
            ),
            (
                'first',
                422,
                lazy_fixture("token_with_edit_scope")   
            )         
        ]
    )
    async def test_deleting_product(
        self,
        client: AsyncClient,
        fake_product_id: int,
        expected_status_code: int,
        token: str | None
    ):
        headers = None
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
        
        response = await client.delete(
            url=f'/products/{fake_product_id}/',
            headers=headers
        )

        assert response.status_code == expected_status_code
