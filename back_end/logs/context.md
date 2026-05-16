# logs/

This folder contains only log files written by the running FastAPI application. Do not commit log files.

| File | Purpose |
|---|---|
| `app.log` | Rotating log file. Every HTTP request (method, path, status code) is logged. The `/hello` endpoint also logs its full response payload. Max 10MB per file, 5 rotated files kept. Created automatically when the server starts. |
| `context.md` | This file. |
