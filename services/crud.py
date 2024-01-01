from sqlalchemy import select


async def get_records_from_db(model, session):
    """
    Выводит записи из бд
    """
    result = await session.execute(select(model).order_by(model.id))
    return result.scalars().all()


async def create_a_record_in_the_db(model, session, **kwargs):
    """
    Создает запись в бд
    """
    db = model(**kwargs)
    session.add(db)
    await session.commit()


async def update_a_record_in_the_db(pk, model, session, **kwargs):
    """
    Обновить запись в бд
    """
    db = await session.get(model, pk)
    for attr, value in kwargs.items():
        setattr(db, attr, value)
    await session.commit()


async def delete_a_record_in_the_db(pk, model, session):
    """
    Удалить запись из бд
    """
    db = await session.get(model, pk)
    await session.delete(db)
    await session.commit()
