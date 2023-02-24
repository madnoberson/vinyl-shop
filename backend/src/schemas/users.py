from typing import Optional

from pydantic import BaseModel

from .products import BasicProduct

class BasicUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    
    scopes: list[str]


class User(BasicUser):
    wishlist_count: int


class UserWishlist(BaseModel):
    products: list[BasicProduct]


class UserWishlistOut(BaseModel):
    wishlist: UserWishlist


class UserOut(BaseModel):
    user: User
    wishlist: UserWishlist


