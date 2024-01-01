from fastapi import APIRouter, Request, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.settings import settings

import orm
from services import crud

item_router = APIRouter(prefix='/items')


@item_router.get("/", name='items')
async def home(request: Request, session: AsyncSession = Depends(orm.get_session)):
    """
    Страница выводит все данные с ItemModel
    """
    items = await crud.get_records_from_db(model=orm.ItemModel, order=orm.ItemModel.user_id, session=session)
    return settings.templates.TemplateResponse("item/index_item.html", {"request": request, "items": items})


@item_router.post("/add")
async def add(
        request: Request,
        item_name: str = Form(...),
        description: str = Form(...),
        user_id: int = Form(...),
        session: AsyncSession = Depends(orm.get_session)
):
    await crud.create_a_record_in_the_db(
        model=orm.ItemModel, item_name=item_name, description=description, user_id=int(user_id), session=session
    )
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)


@item_router.get("/addnew", name='create_item')
async def addnew(request: Request):
    return settings.templates.TemplateResponse("item/create_item.html", {"request": request})


@item_router.get("/edit/{item_id}")
async def edit(
        request: Request,
        item_id: int,
        session: AsyncSession = Depends(orm.get_session)
):
    """
    Берем одну запись с ItemModel, для того чтобы на основе этого выполнять update
    """
    item = await session.get(orm.ItemModel, item_id)
    return settings.templates.TemplateResponse("item/update_item.html", {"request": request, "item": item})


@item_router.post("/update/{item_id}")
async def update(
        request: Request,
        item_id: int,
        item_name: str = Form(...),
        description: str = Form(...),
        user_id: int = Form(...),
        session: AsyncSession = Depends(orm.get_session)
):
    """
    Обновляем запись в ItemModel
    """
    await crud.update_a_record_in_the_db(
        pk=item_id, model=orm.ItemModel, session=session, item_name=item_name, description=description,
        user_id=int(user_id)
    )
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)


@item_router.get("/delete/{item_id}")
async def delete(request: Request, item_id: int, session: AsyncSession = Depends(orm.get_session)):
    """
    Удаляем запись в ItemModel
    """
    await crud.delete_a_record_in_the_db(pk=item_id, model=orm.ItemModel, session=session)
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)
