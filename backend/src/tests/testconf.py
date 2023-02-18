import pytest
from asyncpg import Connection
from httpx import AsyncClient

from ..app import app
from ..database import (
    get_db_conn,
    create_tables,
    create_functions,
)