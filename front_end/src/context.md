# src/

| File/Folder | Purpose |
|---|---|
| `main.jsx` | React entry point — mounts `<App />` into `#root`. |
| `App.jsx` | Root component. Sets up React Router with all routes. Wraps `/home` in `ProtectedRoute`. |
| `pages/` | Full-page route components: SignUp, Login, Home. |
| `components/` | Reusable UI components: ProtectedRoute. |
| `api/` | Axios client configuration with silent refresh interceptor. |
| `context.md` | This file. |
