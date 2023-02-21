from pydantic import BaseModel, validator

from .users import BasicUser


class SuperUser(BaseModel):
    user: BasicUser
    scopes: int


class SuperUserIn(BaseModel):
    user_id: int
    scopes: int

    @validator('scopes')
    def get_scopes_sum(scopes_list: list[int]) -> int:
        return sum(scopes_list)


class SuperUserOut(BaseModel):
    superuser: SuperUser