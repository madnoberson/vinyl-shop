import pytest
from httpx import AsyncClient


@pytest.fixture(scope='class')
def fake_user_wishlist() -> dict:
    return {
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
    def __init__(
        self,
        client: AsyncClient,
        fake_user_token: str,
        fake_user: dict
    ):
        self.client = client
        self.fake_user_token = fake_user_token
        self.fake_user = fake_user

    async def test_getting_user_with_no_token(self):
        response = await self.client.get(
            url='/user/'
        )

        assert response.status_code == 401

    async def test_getting_user_with_token(self):
        response = await self.client.get(
            url='/user/',
            headers={
                "Authorization": f"Bearer {self.fake_user_token}"
            }
        )

        assert response.status_code == 200
        assert response.json() == self.fake_user

    @pytest.mark.parametrize(
        "fake_product_id,expected_status_code",
        [(1, 200), (2, 404), (-1, 422), (1, 409)]
    )
    async def test_adding_product_to_user_wishlist(
        self,
        fake_product_id: int,
        expected_status_code: dict
    ):
        response = await self.client.post(
            url='/users/wishlist/',
            params={
                "product_id": fake_product_id
            },
            headers={
                "Authorization": f"Bearer {self.fake_user_token}"
            }
        )

        assert response.status_code == expected_status_code

    async def test_getting_wishlist(self):
        response = await self.client.get(
            url='/users/wishlist/',
            headers={
                "Authorization": f"Bearer {self.fake_user_token}"
            }
        )

        assert response.status_code == 200
        assert response.json() == {}

    @pytest.mark.parametrize(
        "fake_product_id,expected_status_code",
        [(1, 200), (2, 404), (-1, 422)]
    )
    async def test_deleting_product_from_user_wishlist(
        self,
        fake_product_id: int,
        expected_status_code: dict
    ):
        response = await self.client.delete(
            '/users/wishlist/',
            params={
                "product_id": fake_product_id
            },
            headers={
                "Authorization": f"Bearer {self.fake_user_token}"
            }
        )

        assert response.status_code == expected_status_code