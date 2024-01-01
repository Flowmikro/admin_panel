from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.settings import settings

import orm
from services import crud

item_router = APIRouter(prefix='/items')


@item_router.get("/", name='items')
async def home(request: Request,
               db: AsyncSession = Depends(orm.get_session)):
    users = await db.execute(select(orm.ItemModel).order_by(orm.ItemModel.id))
    items = users.scalars().all()
    return settings.templates.TemplateResponse("item/index_item.html", {"request": request, "items": items})


@item_router.post("/add")
async def add(request: Request, item_name: str = Form(...), description: str = Form(...),
              session: AsyncSession = Depends(orm.get_session)):
    await crud.create_a_record_in_the_db(model=orm.ItemModel, session=session, item_name=item_name,
                                         description=description)
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)


@item_router.get("/addnew", name='create_item')
async def addnew(request: Request):
    return settings.templates.TemplateResponse("item/create_item.html", {"request": request})


@item_router.get("/edit/{item_id}")
async def edit(request: Request, item_id: int, db: AsyncSession = Depends(orm.get_session)):
    item = await db.get(orm.ItemModel, item_id)
    return settings.templates.TemplateResponse("item/update_item.html", {"request": request, "item": item})


@item_router.post("/update/{item_id}")
async def update(request: Request, item_id: int, item_name: str = Form(...), description: str = Form(...),
                 session: AsyncSession = Depends(orm.get_session)):
    await crud.update_a_record_in_the_db(pk=item_id, model=orm.ItemModel, session=session, item_name=item_name,
                                         description=description)
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)


@item_router.get("/delete/{item_id}")
async def delete(request: Request, item_id: int, session: AsyncSession = Depends(orm.get_session)):
    await crud.delete_a_record_in_the_db(pk=item_id, model=orm.ItemModel, session=session)
    return RedirectResponse(url=item_router.url_path_for("items"), status_code=status.HTTP_303_SEE_OTHER)
