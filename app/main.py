from fastapi import FastAPI

from contextlib import asynccontextmanager

from .routers.auth_router import auth_router
from .routers.order_router import order_router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    from .database.session import create_tables
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router=auth_router)
app.include_router(router=order_router)
