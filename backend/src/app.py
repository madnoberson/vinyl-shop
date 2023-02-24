from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.admin import router as admin_router
from .routes.products import router as products_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(products_router)
