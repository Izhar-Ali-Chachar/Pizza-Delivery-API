from pydantic import BaseModel


class DeliveryBase(BaseModel):
    name: str
    vehicle_number: str
    phone_number: str
    email: str
    is_available: bool = True

class DeliveryCreate(DeliveryBase):
    password: str

class DeliveryRead(DeliveryBase):
    id: str

    class Config:
        orm_mode = True