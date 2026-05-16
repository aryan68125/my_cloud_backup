# database/

| File | Purpose |
|---|---|
| `database_models.py` | SQLAlchemy ORM models: `UserMaster`, `UserProfile`, `RefreshToken`. Each class maps directly to a database table. |
| `database_handler.py` | Creates the async connection pool (`engine`) with `pool_size=10`. Defines `get_db()` — a FastAPI dependency generator that yields an `AsyncSession`, commits on success, and rolls back on error. |
| `context.md` | This file. |
