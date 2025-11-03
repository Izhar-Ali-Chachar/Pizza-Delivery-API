from pydantic import BaseModel, Field

from uuid import UUID

from ..database.models import OrderStatus, PizzaSize

class OrderBase(BaseModel):
    name: str
    quantity: int
    pizza_size: PizzaSize = Field(default=PizzaSize.MEDIUM)

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: UUID
    user_id: UUID
    order_status: OrderStatus

class OrderUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None
    pizza_size: PizzaSize | None = None
    order_status: OrderStatus | None = None