import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.database_models import Base, RefreshToken, UserMaster, UserProfile


@pytest.mark.asyncio
async def test_user_master_table_creation():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncTestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncTestSession() as session:
        user = UserMaster(email="test@example.com", password_hash="hashed")
        session.add(user)
        await session.commit()
        assert user.id is not None
        assert user.is_account_disabled is False
        assert user.is_admin_user is False

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_profile_links_to_user_master():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncTestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncTestSession() as session:
        user = UserMaster(email="profile@example.com", password_hash="hashed")
        session.add(user)
        await session.flush()
        profile = UserProfile(user_id=user.id, first_name="Ada", last_name="Lovelace")
        session.add(profile)
        await session.commit()
        assert profile.user_id == user.id

    await engine.dispose()
