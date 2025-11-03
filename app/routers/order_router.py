from fastapi import APIRouter

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@order_router.get("/")
async def read_order_root():
    return {"message": "Order root endpoint"}