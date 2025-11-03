from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str = Field(..., description="The unique identifier of the user")