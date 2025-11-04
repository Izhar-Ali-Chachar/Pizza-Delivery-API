import jwt

from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from typing import Annotated

from .database.models import User, Driver
from .database.session import get_session

from .core.security_settings import oauth2_scheme_user, oauth2_scheme_driver

from .config import jwt_settings

# Alias for database session    
sessionDep = Annotated[AsyncSession, Depends(get_session)]


async def user_access_token(token: Annotated[str | None, Depends(oauth2_scheme_user)]):
    """
    Extract and decode JWT access token.
    """
    try:
        payload = jwt.decode(token, jwt_settings.JWT_SECRET_KEY, algorithms=[jwt_settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return payload

async def driver_access_token(token: Annotated[str | None, Depends(oauth2_scheme_driver)]):
    """
    Extract and decode JWT access token.
    """
    try:
        payload = jwt.decode(token, jwt_settings.JWT_SECRET_KEY, algorithms=[jwt_settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return payload


async def get_current_user(
    session: sessionDep,
    token_data: dict = Depends(user_access_token),
) -> User:
    """
    Extracts current user from JWT and loads from DB.
    """ 
    user_id: str = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    result = await session.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

async def get_current_driver(
    session: sessionDep,
    token_data: dict = Depends(driver_access_token),
) -> Driver:
    """
    Extracts current driver from JWT and loads from DB.
    """
    user_id: str = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    result = await session.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Driver not found")

    return user


currentUserDep = Annotated[User, Depends(get_current_user)]
currentDriverDep = Annotated[User, Depends(get_current_driver)]
