import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient
import asyncpg


@pytest.fixture(scope='class', autouse=True)
async def create_product():
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    await db_conn.execute(
        """
            INSERT INTO products
            (
                name
            )
            VALUES
            (
                'In the Court of the Crimson King'
            )
        """
    )


@pytest.fixture(scope='class')
def get_fake_user_output(
    fake_users_data: dict
):
    fake_user_data = fake_users_data['ivan@ivanov.com'] | \
                     {"wishes_count": 0} | {"id": 3} | \
                     {"email": 'ivan@ivanov.com'}
    fake_user_data.pop("password")

    return {
        "user": fake_user_data,
        "wishlist": {
            "products": []
        }
    }


@pytest.fixture(scope='class')
def get_fake_user_output2(
    fake_users_data: dict
):
    fake_user_data = fake_users_data['fred@nurk.com'] | \
                     {"wishes_count": 1} | {"id": 4} | \
                     {"email": 'fred@nurk.com'}
    fake_user_data.pop("password")

    return {
        "user": fake_user_data,
        "wishlist": {
            "products": [
                {
                    "id": 1,
                    "name": "In the Court of the Crimson King"
                }
            ]
        }
    }
    


@pytest.mark.anyio
class TestUsersService:
    
    @pytest.mark.parametrize(
        [
            "fake_product_id",
            "expected_status_code",
            "token"
        ],
        [
            (
                "first",
                422,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                1,
                401,
                None
            ),
            (
                1,
                201,
                lazy_fixture("token_with_no_scopes2")
            ),
            (
                -1,
                404,
                lazy_fixture("token_with_no_scopes")
            )
        ]
    )
    async def test_adding_product_to_wishlist(
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
        params = {
            "product_id": fake_product_id
        }

        response = await client.post(
            "/user/wishlist/",
            params=params,
            headers=headers
        )

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        [
            "expected_status_code",
            "expected_output",
            "token"
        ],
        [
            (
                401,
                None,
                None
            ),
            (
                200,
                lazy_fixture("get_fake_user_output"),
                lazy_fixture("token_with_no_scopes")
            ),
            (
                200,
                lazy_fixture("get_fake_user_output2"),
                lazy_fixture("token_with_no_scopes2")
            )

        ]
    )
    async def test_getting_user(
        self,
        client: AsyncClient,
        expected_status_code: int,
        expected_output: dict | None,
        token: str
    ):
        headers = {}
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
        
        response = await client.get(
            url='/user/',
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
                404,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                "first",
                422,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                -1,
                404,
                lazy_fixture("token_with_no_scopes2")
            ),
            (
                1,
                204,
                lazy_fixture("token_with_no_scopes2")
            )
        ]
    )
    async def test_deleting_product_from_wishlist(
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
        
        params = {
            "product_id": fake_product_id
        }

        response = await client.delete(
            url="/user/wishlist/",
            params=params,
            headers=headers
        )

        assert response.status_code == expected_status_code
