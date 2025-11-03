from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.get("/")
async def read_auth_root():
    return {"message": "Auth root endpoint"}