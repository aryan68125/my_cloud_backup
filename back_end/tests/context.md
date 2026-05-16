# tests/

| File | Purpose |
|---|---|
| `conftest.py` | Pytest fixtures: `db_engine` (in-memory SQLite), `client` (HTTPX async client with DB override), `db_session` (direct DB access for test setup). Sets all required env vars before imports. |
| `test_models.py` | Smoke tests for SQLAlchemy ORM models — verifies table creation and FK relationships. |
| `test_auth_handler.py` | Unit tests for pure auth functions: password hashing, JWT creation/verification, refresh token generation. |
| `test_auth.py` | Integration tests for all `/auth/*` endpoints: signup, login (including disabled account), refresh, logout. |
| `test_user.py` | Integration tests for all `/user/*` endpoints: get me, update profile, delete account. |
| `test_hello.py` | Integration test for `GET /hello`. |
| `context.md` | This file. |
