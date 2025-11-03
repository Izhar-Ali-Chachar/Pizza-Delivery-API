from fastapi import FastAPI

from .routers.auth_router import auth_router
from .routers.order_router import order_router

app = FastAPI()

app.include_router(router=auth_router)
app.include_router(router=order_router)
