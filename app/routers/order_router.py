from fastapi import APIRouter

from sqlmodel import select

from ..schemas.order import OrderCreate, OrderRead, OrderUpdate

from ..dependencies import sessionDep, currentUserDep
from ..database.models import Order

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@order_router.get("/", response_model=list[OrderRead])
async def get_orders(session: sessionDep):
    """
    Get all orders (admin use)
    """
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return orders

@order_router.post("/create", response_model=OrderRead)
async def create_order(order: OrderCreate, session: sessionDep, current_user: currentUserDep):
    db_order = Order(
        **order.model_dump(), 
        user_id=current_user.id,
        order_status="pending"
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    return db_order
