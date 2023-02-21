import pytest
from asyncpg import UndefinedTableError
from httpx import AsyncClient

from ..app import app
from ..database import (
    create_tables,
    create_functions,
    clean_up_db
)


@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope='function', autouse=True)
async def refresh_db() -> None:
    try:
        await clean_up_db()
    except UndefinedTableError:
        pass

    await create_tables()
    await create_functions()


@pytest.fixture
async def fake_user_1() -> dict:
    return {
        "name": "john",
        "last_name": "doe"
    }


@pytest.fixture
async def fake_user_2() -> dict:
    return {
        "name": "jane",
        "last_name": "doe"
    }


@pytest.fixture
async def fake_product() -> dict:
    return {
        "name": "In the Court of the Crimson King "
    }


@pytest.fixture
async def token_with_edit_scope() -> str:
    pass


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
