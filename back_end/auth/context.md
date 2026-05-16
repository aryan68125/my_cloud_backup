# auth/

| File | Purpose |
|---|---|
| `auth_handler.py` | Pure functions with no FastAPI dependencies: `hash_password`, `verify_password`, `create_access_token`, `create_refresh_token`, `verify_access_token`, `set_auth_cookies`, `clear_auth_cookies`. Used by both the auth router and user handler. |
| `auth_router.py` | FastAPI router at prefix `/auth` with Swagger tag `Auth`. Endpoints: `POST /signup`, `POST /login`, `POST /refresh`, `POST /logout`. |
| `context.md` | This file. |
