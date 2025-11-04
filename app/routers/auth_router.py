from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

import jwt

from sqlmodel import select

from ..dependencies import sessionDep
from ..database.models import User

from ..schemas.user import UserCreate

from ..config import jwt_settings

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.post("/sign-up")
async def sign_up(user_create: UserCreate, session: sessionDep):
    new_user = User(
        **user_create.model_dump(exclude=("password",)),
        hashed_password=pwd_context.hash(user_create.password)  # In a real app, hash the password!
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@auth_router.post("/sign-in")
async def sign_in(session: sessionDep, request_form: OAuth2PasswordRequestForm = Depends()):
    result = await session.execute(
        select(User).where(User.email == request_form.username)
    )

    user = result.scalar()

    if user is None or not pwd_context.verify(request_form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    payload = {"sub": str(user.id), "name": user.name}

    token = jwt.encode(
        payload,
        key=jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}
    