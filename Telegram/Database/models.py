from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import BigInteger, String

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

session = async_sessionmaker(bind=engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    is_premium: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    username = mapped_column(String(37))
    nickname = mapped_column(String(300))


async def database_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
