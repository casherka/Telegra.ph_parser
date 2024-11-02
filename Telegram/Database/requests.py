from Telegram.Database.models import session
from Telegram.Database.models import User
from sqlalchemy import select


async def set_user(tg_id: int, username: str, nickname: str):
    async with session() as lsession:
        user = await lsession.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            lsession.add(User(tg_id=tg_id, username=username, nickname=nickname.replace('None', '')))
            await lsession.commit()


async def get_premium(tg_id: int):
    async with session() as lsession:
        user = await lsession.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            lsession.add(User(tg_id=tg_id))
            await lsession.commit()
        else:
            premium = await lsession.scalar(select(User).where(User.tg_id == tg_id).where(User.is_premium))
    return bool(premium)


async def get_admin(tg_id: int):
    async with session() as lsession:
        user = await lsession.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            lsession.add(User(tg_id=tg_id))
            await lsession.commit()
        else:
            admin = await lsession.scalar(select(User).where(User.tg_id == tg_id).where(User.is_admin))
    return bool(admin)
