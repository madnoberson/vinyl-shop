import pytest
import asyncpg
from asyncpg import UndefinedTableError
from httpx import AsyncClient

from ..app import app
from ..database import (
    create_tables,
    create_functions,
    clean_up_db
)
from ..utils import scopes, sql_utils


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope='session')
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as client:
        yield client



@pytest.fixture(scope='session')
async def fake_users_data() -> list[dict[str, dict[str, str]]]:
    return {
        "john@doe.com": {
            "first_name": "john",
            "last_name": "doe",
            "password": "secret",
            "scopes": ["admin"]
        },
        "jane@doe.com": {
            "first_name": "jane",
            "last_name": "doe",
            "password": "secret",
            "scopes": ["edit"]
        },
        "ivan@ivanov.com": {
            "first_name": "ivan",
            "last_name": "ivanov",
            "password": "secret",
            "scopes": []
        }
    }


@pytest.fixture(scope='module', autouse=True)
async def refresh_db() -> None:
    try:
        await clean_up_db()
    except UndefinedTableError:
        pass

    await create_tables()
    await create_functions()


@pytest.fixture(scope='module', autouse=True)
async def register_fake_users_and_give_them_privileges(
    client: AsyncClient,
    fake_users_data: dict[str, dict[str, str]]
):
    fake_superusers_data = []
    id = 0
    for email, user_data in fake_users_data.items():
        input = {
            "first_name": user_data["first_name"],
            "last_name": user_data['last_name'],
            "email": email,
            "password": user_data['password']
        }

        await client.post(
            url='/sign_up/',
            json=input
        )

        id += 1
        if not user_data['scopes']:
            continue
        
        fake_superusers_data.append(
            {
                "id": id,
                "scopes": scopes.get_scopes_sum_from_scopes(
                    scopes=user_data['scopes']
                )
            }
        )

    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    values_list = []
    for data in fake_superusers_data:
        _, values = sql_utils.dict_to_sql_columns_and_values(
            data
        )
        values_list.append(values)
    
    values = ','.join(values_list)
    await db_conn.execute(
        f"""
            INSERT INTO superusers
            (
                user_id,
                scopes
            )
            VALUES
            {values}
        """
    ) 


@pytest.fixture(scope='module')
async def users_tokens(
    fake_users_data: dict,
    client: AsyncClient
) -> dict[str, str]:
    fake_users_tokens = {}
    for email, user_data in fake_users_data.items():
        input = {
            "email": email,
            "password": user_data['password']
        }

        response = await client.post(
            url='/sign_in/',
            json=input
        )

        token = response.json()['access_token']
        fake_users_tokens[email] = token

    return fake_users_tokens


@pytest.fixture(scope='module')
async def token_with_admin_scope(
    users_tokens: dict
) -> str:
    return users_tokens['john@doe.com']


@pytest.fixture(scope='module')
async def token_with_edit_scope(
    users_tokens: dict
) -> str:
    return users_tokens['jane@doe.com']


@pytest.fixture(scope='module')
async def token_with_no_scopes(
    users_tokens: dict
) -> str:
    return users_tokens['ivan@ivanov.com']