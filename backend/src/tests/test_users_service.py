import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient


@pytest.fixture(scope='class')
def get_fake_user_wishlist_output() -> dict:
    return {
            "products": [],
            "products_count": 0
        }


@pytest.fixture(scope='class')
def get_fake_user2_wishlist_output(
    fake_product_basic_data: dict
) -> dict:
    return {
        "products": [
            fake_product_basic_data
        ],
        "products_count": 1
    }


@pytest.fixture(scope='class')
def get_fake_user_cart_output() -> dict:
    return {
        "products": [],
        "products_count": 0
    }


@pytest.fixture(scope='class')
def get_fake_user2_cart_output(
    fake_product_basic_data: dict
) -> dict:
    return {
        "products": [
            fake_product_basic_data
        ],
        "products_count": 1
    }


@pytest.fixture(scope='class')
def get_fake_user_output(
    fake_common_user_data: dict,
    get_fake_user_wishlist_output: dict
) -> dict:
    return {
        "user": fake_common_user_data,
        "wishlist": get_fake_user_wishlist_output
    }


@pytest.fixture(scope='class')
def get_fake_user2_output(
    fake_common_user2_data: dict,
    get_fake_user2_wishlist_output: dict
) -> dict:
    return {
        "user": fake_common_user2_data,
        "wishlist": get_fake_user2_wishlist_output
    }


@pytest.mark.usefixtures("create_fake_product")
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
                lazy_fixture("get_fake_user2_output"),
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
                -1,
                404,
                lazy_fixture("token_with_no_scopes")
            ),
            (
                1,
                201,
                lazy_fixture("token_with_no_scopes2")
            )
        ]
    )
    async def test_adding_product_to_cart(
        self,
        client: AsyncClient,
        fake_product_id: int,
        expected_status_code: int,
        token: int | None
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
            url='/user/cart/',
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
                lazy_fixture("get_fake_user_cart_output"),
                lazy_fixture("token_with_no_scopes")
            ),
            (
                200,
                lazy_fixture("get_fake_user2_cart_output"),
                lazy_fixture("token_with_no_scopes2")
            )
        ]
    )
    async def test_getting_cart(
        self,
        client: AsyncClient,
        expected_status_code: int,
        expected_output: dict | None,
        token: str | None
    ):
        headers = None
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
        
        response = await client.get(
            url='/user/cart/',
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
    async def test_deleting_product_from_cart(
        self,
        client: AsyncClient,
        fake_product_id: int,
        expected_status_code: int,
        token: int | None
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
            url='/user/cart/',
            params=params,
            headers=headers
        )

        assert response.status_code == expected_status_code
