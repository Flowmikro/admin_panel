import contextlib
from typing import AsyncIterator
from fastapi import FastAPI

import orm
import router
from app.settings import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    orm.db_manager.init(settings.database_url)
    yield
    await orm.db_manager.close()


app = FastAPI(title="Admin API", lifespan=lifespan)

app.include_router(router.home_router)
app.include_router(router.user_router)
app.include_router(router.item_router)
app.include_router(router.auth_router)
