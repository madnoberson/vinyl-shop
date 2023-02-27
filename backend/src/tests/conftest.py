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
async def fake_users_data() -> dict[str, dict[str, str]]:
    return {
        "fake_user_with_admin_scope": {
            "id": 1,
            "first_name": "john",
            "last_name": "doe",
            "email": "john@doe.com",
            "password": "secret",
            "scopes": ["admin"]
        },
        "fake_user_with_edit_scope": {
            "id": 2,
            "first_name": "jane",
            "last_name": "doe",
            "email": "jane@doe.com",
            "password": "secret",
            "scopes": ["edit"]
        },
        "fake_common_user": {
            "id": 3,
            "first_name": "ivan",
            "last_name": "ivanov",
            "email": "ivan@ivanov.com",
            "password": "secret",
            "scopes": []
        },
        "fake_common_user2": {
            "id": 4,
            "first_name": "fred",
            "last_name": "nurk",
            "email": "fred@nurk.com",
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
    for id, user_data in enumerate(fake_users_data.values()):
        input = {
            "first_name": user_data["first_name"],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": user_data['password']
        }

        await client.post(
            url='/sign_up/',
            json=input
        )

        if not user_data['scopes']:
            continue
        
        fake_superusers_data.append(
            {
                "id": id + 1,
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
    for user, user_data in fake_users_data.items():
        input = {
            "email": user_data['email'],
            "password": user_data['password']
        }

        response = await client.post(
            url='/sign_in/',
            json=input
        )

        token = response.json()['access_token']
        fake_users_tokens[user] = token

    return fake_users_tokens


@pytest.fixture(scope='module')
async def fake_user_with_admin_scope_data(
    fake_users_data: dict
) -> dict:
    user_data = fake_users_data['fake_user_with_admin_scope']
    user_data.pop('password')

    return user_data 


@pytest.fixture(scope='module')
async def token_with_admin_scope(
    users_tokens: dict
) -> str:
    return users_tokens['fake_user_with_admin_scope']


@pytest.fixture(scope='module')
async def fake_user_with_edit_scope_data(
    fake_users_data: dict
) -> dict:
    user_data = fake_users_data['fake_user_with_edit_scope']
    user_data.pop('password')

    return user_data


@pytest.fixture(scope='module')
async def token_with_edit_scope(
    users_tokens: dict
) -> str:
    return users_tokens['fake_user_with_edit_scope']


@pytest.fixture(scope='module')
async def fake_common_user_data(
    fake_users_data: dict
) -> dict:
    user_data = fake_users_data['fake_common_user']
    user_data.pop('password')

    return user_data


@pytest.fixture(scope='module')
async def token_with_no_scopes(
    users_tokens: dict
) -> str:
    return users_tokens['fake_common_user']


@pytest.fixture(scope='module')
async def fake_common_user2_data(
    fake_users_data: dict
) -> dict:
    user_data = fake_users_data['fake_common_user2']
    user_data.pop('password')

    return user_data


@pytest.fixture(scope='module')
async def token_with_no_scopes2(
    users_tokens: dict
) -> str:
    return users_tokens['fake_common_user2']


@pytest.fixture(scope='class')
async def fake_product_basic_data() -> dict:
    return {
        "id": 1,
        "name": "In the Court of the Crimson King"
    }


@pytest.fixture(scope='class')
async def create_fake_product(
    fake_product_basic_data: dict
):
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    await db_conn.execute(
        f"""
            INSERT INTO products
            (
                name
            )
            VALUES
            (
                '{fake_product_basic_data['name']}'
            )
        """
    )