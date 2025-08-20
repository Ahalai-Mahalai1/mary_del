from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import declarative_base
import random

Base = declarative_base()
sessionmaker = None

class User(Base):
    __tablename__ = "channel_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)

async def init_db(db_url: str):
    global sessionmaker
    engine = create_async_engine(db_url, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user(user_id: int):
    async with sessionmaker() as session:
        exists = await session.get(User, {"user_id": user_id})
        if not exists:
            session.add(User(user_id=user_id))
            await session.commit()

async def get_random_user():
    async with sessionmaker() as session:
        result = await session.execute(
            User.__table__.select()
        )
        users = result.fetchall()
        if users:
            return random.choice(users)
        return None

async def remove_user(user_id: int):
    async with sessionmaker() as session:
        await session.execute(
            User.__table__.delete().where(User.user_id == user_id)
        )
        await session.commit()