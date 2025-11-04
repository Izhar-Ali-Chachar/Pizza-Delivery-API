from pydantic import BaseModel, EmailStr, Field

from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID = Field(..., description="The unique identifier of the user")