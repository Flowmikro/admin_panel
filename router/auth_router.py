from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, Response, responses, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import orm
from app.settings import settings
from auth.form import LoginForm, UserCreateForm
from auth.schemas import UserCreateSchema, Token
from auth.services import create_access_token, create_new_user
from auth.utils import authenticate_user

auth_router = APIRouter()


@auth_router.get("/new_user", name='new_user')
def register(request: Request):
    """
    Вызывает страницу register.html
    """
    return settings.templates.TemplateResponse("auth/register.html", {"request": request})


@auth_router.post("/new_user")
async def register(request: Request, session: AsyncSession = Depends(orm.get_session)):
    """
    Проверка заполнение формы и сохранение записи в UserModel
    """
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreateSchema(
            username=form.username, email=form.email, password=form.password
        )
        try:
            await create_new_user(user=user, session=session)
            return responses.RedirectResponse(
                "/user/", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            form.__dict__.get("errors").append("Имя пользователя или адрес электронной почты заняты")
            return settings.templates.TemplateResponse("auth/register.html", form.__dict__)
    return settings.templates.TemplateResponse("auth/register.html", form.__dict__)


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(orm.get_session)):
    """
    Модем проверить/просмотреть токен. Доступно в /docs
    """
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}",
                        httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/login")
def login(request: Request):
    """
    Вызывает страницу login.html
    """
    return settings.templates.TemplateResponse("auth/login.html", {"request": request})


@auth_router.post("/login")
async def login(request: Request, session: AsyncSession = Depends(orm.get_session)):
    """
    Проверка данных пользователя
    """
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = settings.templates.TemplateResponse("auth/login.html", form.__dict__)
            await login_for_access_token(response=response, form_data=form, session=session)
            return responses.RedirectResponse(
                "/user", status_code=status.HTTP_302_FOUND
            )
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Неверный адрес электронной почты или пароль")
            return settings.templates.TemplateResponse("auth/login.html", form.__dict__)
    return settings.templates.TemplateResponse("auth/login.html", form.__dict__)
