from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
sdfds = 'fsdf'

async def get_records_from_db(model, order, session):
    """
    Выводит записи из бд
    """
    result = await session.execute(select(model).order_by(order))
    return result.scalars().all()


async def get_one_record_in_db(pk, model, session):
    """
    Выводит одну запись из бд
    """
    result = await session.get(model, pk)
    return result


async def create_a_record_in_the_db(model, session, **kwargs):
    """
    Создает запись в бд
    """
    try:
        db = model(**kwargs)
        session.add(db)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Проверьте поля')


async def update_a_record_in_the_db(pk, model, session, **kwargs):
    """
    Обновить запись в бд
    """
    try:
        db = await session.get(model, pk)
        for attr, value in kwargs.items():
            setattr(db, attr, value)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Проверьте поля')


async def delete_a_record_in_the_db(pk, model, session):
    """
    Удалить запись из бд
    """
    db = await session.get(model, pk)
    await session.delete(db)
    await session.commit()

f = []