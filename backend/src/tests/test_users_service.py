# import pytest
# from pytest_lazyfixture import lazy_fixture
# from httpx import AsyncClient


# @pytest.fixture(scope='class')
# def fake_user_wishlist() -> dict:
#     return {
#         "wishlist": {
#             "products": [
#                 {
#                     "id": 1,
#                     "name": "In the Court of the Crimson King"
#                 }
#             ]
#         }
#     }


# @pytest.mark.anyio
# class TestUsersService:

#     @pytest.mark.parametrize(
#         "fake_token, expected_status_code, fake_user_data",
#         [
#             (lazy_fixture("fake_user_token"), 200, lazy_fixture("fake_user")),
#             (None, 401, None)
#         ]
#     )
#     async def test_getting_user(
#         self,
#         expected_status_code: int,
#         client: AsyncClient,
#         fake_token: str | None,
#         fake_user_data: dict | None,
#     ):
#         headers = None
#         if fake_token:
#             headers={
#                 "Authorization": f"Bearer {fake_token}"
#             }

#         response = await client.get(
#             url='/user/',
#             headers=headers  
#         )

#         assert response.status_code == expected_status_code

#         if fake_user_data:
#             assert response.json() == fake_user_data

    # @pytest.mark.parametrize(
    #     "fake_product_id,expected_status_code",
    #     [(1, 200), (2, 404), (-1, 422), (1, 409)]
    # )
    # async def test_adding_product_to_user_wishlist(
    #     self,
    #     client: AsyncClient,
    #     fake_product_id: int,
    #     expected_status_code: dict,
    #     fake_user_token: str
    # ):
    #     response = await client.post(
    #         url='/users/wishlist/',
    #         params={
    #             "product_id": fake_product_id
    #         },
    #         headers={
    #             "Authorization": f"Bearer {fake_user_token}"
    #         }
    #     )

    #     assert response.status_code == expected_status_code

    # async def test_getting_wishlist(self):
    #     response = await self.client.get(
    #         url='/users/wishlist/',
    #         headers={
    #             "Authorization": f"Bearer {self.fake_user_token}"
    #         }
    #     )

    #     assert response.status_code == 200
    #     assert response.json() == {}

    # @pytest.mark.parametrize(
    #     "fake_product_id,expected_status_code",
    #     [(1, 200), (2, 404), (-1, 422)]
    # )
    # async def test_deleting_product_from_user_wishlist(
    #     self,
    #     fake_product_id: int,
    #     expected_status_code: dict
    # ):
    #     response = await self.client.delete(
    #         '/users/wishlist/',
    #         params={
    #             "product_id": fake_product_id
    #         },
    #         headers={
    #             "Authorization": f"Bearer {self.fake_user_token}"
    #         }
    #     )

    #     assert response.status_code == expected_status_code