# api/

| File | Purpose |
|---|---|
| `client.js` | Pre-configured Axios instance with `baseURL=/api` and `withCredentials=true`. Response interceptor catches 401s, calls `POST /api/auth/refresh` once, retries the original request on success, redirects to `/login` if refresh fails. Handles concurrent 401s with a queue to avoid duplicate refresh calls. |
| `context.md` | This file. |
