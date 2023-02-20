from pydantic import BaseModel


class BasicUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    
    scopes: list[str]
