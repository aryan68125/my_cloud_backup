# user/

| File | Purpose |
|---|---|
| `user_handler.py` | `get_current_user` FastAPI dependency. Reads `access_token` cookie, calls `verify_access_token`, loads the `UserMaster` row (with profile eager-loaded), and checks `is_account_disabled`. Raises 401 if no token or user not found; 403 if disabled. |
| `user_router.py` | FastAPI router at prefix `/user` with Swagger tag `User`. Endpoints: `GET /me`, `PUT /me`, `DELETE /me`. All require a valid access_token cookie via `get_current_user` dependency. |
| `context.md` | This file. |
