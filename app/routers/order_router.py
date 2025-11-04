from fastapi import APIRouter, HTTPException, status

from sqlmodel import select

from uuid import UUID

from ..schemas.order import OrderCreate, OrderRead, OrderUpdate

from ..dependencies import sessionDep, currentUserDep, adminDep, userDep
from ..database.models import Order

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@order_router.get("/", response_model=list[OrderRead])
async def get_orders(session: sessionDep, current_user: adminDep):
    """
    Get all orders (admin use)
    """
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return orders

@order_router.get('/{id}', response_model=OrderRead)
async def get_order_by_id(id: UUID, session: sessionDep):
    """
    Get order by ID
    """
    result = await session.execute(select(Order).where(Order.id == id))
    order = result.scalar()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return order

@order_router.post("/create", response_model=OrderRead)
async def create_order(order: OrderCreate, session: sessionDep, current_user: userDep):
    db_order = Order(
        **order.model_dump(), 
        user_id=current_user.id,
        order_status="pending"
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    return db_order

@order_router.patch("/update/{id}", response_model=OrderRead)
async def update_order_status(id: UUID, order: OrderUpdate, session: sessionDep):
    """
    Update order by ID (admin use)
    """
    result = await session.execute(select(Order).where(Order.id == id))
    db_order = result.scalar()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    order_data = order.model_dump(exclude_unset=True)
    
    db_order.sqlmodel_update(order_data)

    await session.commit()
    await session.refresh(db_order)
    return db_order

@order_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: UUID, session: sessionDep, current_user: adminDep):
    """
    Delete order by ID (admin use)
    """
    result = await session.execute(select(Order).where(Order.id == id))
    db_order = result.scalar()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    await session.delete(db_order)
    await session.commit()
    return None