# back_end_initialization/

| File | Purpose |
|---|---|
| `seed_data.py` | Runs automatically as part of Docker startup (before uvicorn). Reads `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `.env`. Checks if admin user already exists in `user_master` — inserts if not, skips if found. Fully idempotent. |
| `context.md` | This file. |
