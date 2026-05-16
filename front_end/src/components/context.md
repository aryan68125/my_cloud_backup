# components/

| File | Purpose |
|---|---|
| `ProtectedRoute.jsx` | Wrapper component. On mount, calls `GET /api/user/me` to verify auth. Renders children if authenticated (200), redirects to `/login` if not (401 → silent refresh attempted by Axios interceptor first). Shows nothing while checking. |
| `context.md` | This file. |
