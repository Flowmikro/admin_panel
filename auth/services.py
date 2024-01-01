from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import datetime, timedelta

import orm
from auth.hasher import Hasher
from auth.schemas import UserCreateSchema
from app.settings import settings
from services import crud


async def create_new_user(user: UserCreateSchema, session: AsyncSession = Depends(orm.get_session)):
    await crud.create_a_record_in_the_db(
        model=orm.UserModel, session=session, username=user.username, email=user.email, hashed_password=Hasher.get_password_hash(user.password)
    )
    return user


async def get_user(username: str, session: AsyncSession = Depends(orm.get_session)):
    result = await session.execute(select(orm.UserModel).where(orm.UserModel.email == username))
    result = result.scalars().all()
    if result:
        return result[0]
    return None


async def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
