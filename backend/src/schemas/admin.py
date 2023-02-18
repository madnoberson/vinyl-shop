from pydantic import BaseModel


class Superuser(BaseModel):
    id: int
    name: str
