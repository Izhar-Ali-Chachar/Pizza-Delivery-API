from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

import jwt

from sqlmodel import select

from ..dependencies import sessionDep
from ..database.models import Driver

from ..schemas.delivery import DeliveryCreate

from ..config import jwt_settings

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

delivery_router = APIRouter(
    prefix="/delivery",
    tags=["delivery"],
)

@delivery_router.post("/sign-up")
async def sign_up(delivery_create: DeliveryCreate, session: sessionDep):
    new_delivery = Driver(
        **delivery_create.model_dump(exclude=("password",)),
        hashed_password=pwd_context.hash(delivery_create.password)  # In a real app, hash the password!
    )
    session.add(new_delivery)
    await session.commit()
    await session.refresh(new_delivery)
    return {"message": "Delivery person created successfully", "delivery_id": new_delivery.id}

@delivery_router.post("/sign-in")
async def sign_in(session: sessionDep, request_form: OAuth2PasswordRequestForm = Depends()):
    result = await session.execute(
        select(Driver).where(Driver.email == request_form.username)
    )

    driver = result.scalar()

    if driver is None or not pwd_context.verify(request_form.password, driver.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {"sub": str(driver.id), "name": driver.name}

    token = jwt.encode(
        payload,
        key=jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}
    