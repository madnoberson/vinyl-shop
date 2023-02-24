from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str = 'shdsudosuiyd782wy7802y897yhwoihdisxc9sny27dsuihuisy812'
    jwt_algorithm: str = 'HS256'
    jwt_expires: int = 24 #Hours

    user_wishlist_elems_per_page: int = 10


settings = Settings()