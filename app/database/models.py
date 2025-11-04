from enum import Enum

from pydantic import EmailStr

from sqlalchemy.dialects import postgresql as PostgreSQL
from sqlmodel import Field, Relationship, SQLModel, Column

from uuid import UUID, uuid4

from typing import List, Optional

class UserRole(str, Enum):
    USER = "user"
    DRIVER = "driver"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PostgreSQL.UUID(as_uuid=True), primary_key=True, default=uuid4)
    )
    name: str
    email: EmailStr
    hashed_password: str
    role: UserRole = Field(default=UserRole.USER)

    orders: List["Order"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PizzaSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PostgreSQL.UUID(as_uuid=True), primary_key=True, default=uuid4)
    )
    name: str
    quantity: int
    order_status: OrderStatus = Field(default=OrderStatus.PENDING)
    pizza_size: PizzaSize = Field(default=PizzaSize.MEDIUM)

    user_id: UUID = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(
        back_populates="orders",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
