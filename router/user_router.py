from fastapi import APIRouter, Request, Depends, Form, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from app.settings import settings
from services import crud
import orm

user_router = APIRouter(prefix='/user')


@user_router.get("/", name='user')
async def home(request: Request, session: AsyncSession = Depends(orm.get_session)):
    users = await crud.get_records_from_db(model=orm.UserModel, order=orm.UserModel.id, session=session)
    return settings.templates.TemplateResponse("user/index_user.html", {"request": request, "users": users})


@user_router.post("/add")
async def add(
        request: Request,
        username: str = Form(...),
        email: EmailStr = Form(...),
        hashed_password: str = Form(...),
        session: AsyncSession = Depends(orm.get_session)
):
    await crud.create_a_record_in_the_db(
        model=orm.UserModel, session=session, username=username, email=email, hashed_password=hashed_password
    )
    return RedirectResponse(url=user_router.url_path_for("user"), status_code=status.HTTP_303_SEE_OTHER)


@user_router.get("/addnew")
async def addnew(request: Request):
    return settings.templates.TemplateResponse("user/create_user.html", {"request": request})


@user_router.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: AsyncSession = Depends(orm.get_session)):
    user = await db.get(orm.UserModel, user_id)
    return settings.templates.TemplateResponse("user/update_user.html", {"request": request, "user": user})


@user_router.post("/update/{user_id}")
async def update(
        request: Request,
        user_id: int,
        username: str = Form(...),
        email: EmailStr = Form(...),
        session: AsyncSession = Depends(orm.get_session)
):
    await crud.update_a_record_in_the_db(
        pk=user_id, model=orm.UserModel, session=session, username=username, email=email
    )
    return RedirectResponse(url=user_router.url_path_for("user"), status_code=status.HTTP_303_SEE_OTHER)


@user_router.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, session: AsyncSession = Depends(orm.get_session)):
    await crud.delete_a_record_in_the_db(pk=user_id, model=orm.UserModel, session=session)
    return RedirectResponse(url=user_router.url_path_for("user"), status_code=status.HTTP_303_SEE_OTHER)
