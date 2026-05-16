# db_migrations/

Managed by Alembic. Contains migration scripts that evolve the database schema over time.

| Item | Purpose |
|---|---|
| `env.py` | Alembic environment config. Loads `.env`, imports `Base` from `database_models.py` so Alembic can detect schema changes. Uses async SQLAlchemy engine for online migrations. |
| `script.py.mako` | Template used to generate new migration files. |
| `versions/` | Individual migration files. Each file has an `upgrade()` and `downgrade()` function. |
| `versions/0001_initial_tables.py` | Creates `user_master`, `user_profile`, and `refresh_tokens` tables. |
| `context.md` | This file. |
