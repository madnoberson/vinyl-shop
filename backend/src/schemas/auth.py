from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserSignUp(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str