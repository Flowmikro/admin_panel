from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import orm
from auth.auth_cookie import OAuth2PasswordBearerWithCookie
from auth.hasher import Hasher
from auth.services import get_user

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


async def authenticate_user(username: str, password: str, session: AsyncSession = Depends(orm.get_session)):
    user = await get_user(username=username, session=session)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user
