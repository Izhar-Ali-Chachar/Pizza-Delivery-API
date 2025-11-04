from pydantic import BaseModel, EmailStr, Field

from uuid import UUID

from ..database.models import UserRole

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    role: UserRole = Field(default=UserRole.USER)
    password: str

class UserRead(UserBase):
    id: UUID = Field(..., description="The unique identifier of the user")