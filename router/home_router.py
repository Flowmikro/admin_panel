from fastapi import APIRouter, Request, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import orm
from app.settings import settings

home_router = APIRouter()


@home_router.get('/', name="home")
async def home_count(request: Request, db: AsyncSession = Depends(orm.get_session)):
    result_user = (await db.execute(select(func.count(orm.UserModel.id)))).scalar()
    result_item = (await db.execute(select(func.count(orm.ItemModel.id)))).scalar()
    return settings.templates.TemplateResponse("home.html",
                                               {"request": request, "result_user": result_user,
                                                'result_item': result_item})
