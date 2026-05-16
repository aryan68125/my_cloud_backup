import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../configs/.env"))

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.database_models import UserMaster

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


async def seed() -> None:
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("[seed] ADMIN_EMAIL or ADMIN_PASSWORD not set. Skipping.")
        return

    engine = create_async_engine(_DATABASE_URL)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserMaster).where(UserMaster.email == admin_email)
        )
        if result.scalar_one_or_none():
            print(f"[seed] Admin '{admin_email}' already exists. Skipping.")
        else:
            session.add(
                UserMaster(
                    email=admin_email,
                    password_hash=_pwd_context.hash(admin_password),
                    is_admin_user=True,
                )
            )
            await session.commit()
            print(f"[seed] Admin '{admin_email}' created.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
