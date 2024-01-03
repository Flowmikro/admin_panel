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
    """
    Страница выводит все данные с UserModel
    """
    users = await crud.get_records_from_db(model=orm.UserModel, order=orm.UserModel.id, session=session)
    return settings.templates.TemplateResponse("user/index_user.html", {"request": request, "users": users})


@user_router.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: AsyncSession = Depends(orm.get_session)):
    """
    Берем одну запись с UserModel, для того чтобы на основе этого выполнять update
    """
    user = await crud.get_one_item_in_db(pk=user_id, model=orm.UserModel, session=session)
    return settings.templates.TemplateResponse("user/update_user.html", {"request": request, "user": user})


@user_router.post("/update/{user_id}")
async def update(
        request: Request,
        user_id: int,
        username: str = Form(...),
        email: EmailStr = Form(...),
        session: AsyncSession = Depends(orm.get_session)
):
    """
    Обновляем запись в UserModel
    """
    await crud.update_a_record_in_the_db(
        pk=user_id, model=orm.UserModel, session=session, username=username, email=email
    )
    return RedirectResponse(url=user_router.url_path_for("user"), status_code=status.HTTP_303_SEE_OTHER)


@user_router.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, session: AsyncSession = Depends(orm.get_session)):
    """
    Удаляем запись в UserModel
    """
    await crud.delete_a_record_in_the_db(pk=user_id, model=orm.UserModel, session=session)
    return RedirectResponse(url=user_router.url_path_for("user"), status_code=status.HTTP_303_SEE_OTHER)
