from pydantic import BaseModel, validator

from .products import BasicProduct

from ..utils.scopes import get_scopes_from_scopes_sum


class BasicUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    
    scopes: int | None | list[str]

    @validator('scopes')
    def get_scopes(scopes_sum: int | None) -> list[str]:
        if isinstance(scopes_sum, list):
            return scopes_sum
        if scopes_sum is None:
            return []
        return get_scopes_from_scopes_sum(scopes_sum)


class User(BasicUser):
    pass


class UserWishlist(BaseModel):
    products: list[BasicProduct]
    products_count: int


class UserCart(BaseModel):
    products: list[BasicProduct]
    products_count: int


class UserOut(BaseModel):
    user: User
    wishlist: UserWishlist


