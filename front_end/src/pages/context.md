# pages/

| File | Purpose |
|---|---|
| `SignUp.jsx` | Sign-up form (email + password). Calls `POST /api/auth/signup`. On success, navigates to `/home`. Shows API error messages inline. |
| `Login.jsx` | Login form (email + password). Calls `POST /api/auth/login`. On success, navigates to `/home`. Shows API error messages inline. |
| `Home.jsx` | Protected page. Displays user's full name (or email fallback if no profile). Contains "Say Hello" button (calls `GET /api/hello`) and "Log Out" button (calls `POST /api/auth/logout`). |
| `context.md` | This file. |
