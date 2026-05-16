import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "configs/.env"))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_router import router as auth_router
from user.user_router import router as user_router

# ── Logging ───────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
_file_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5
)
_file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
)
logging.basicConfig(
    level=logging.INFO,
    handlers=[_file_handler, logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="My Cloud Backup API",
    version="1.0.0",
    description="Backend API for My Cloud Backup — user auth and user management.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info("[%s] %s → %s", request.method, request.url.path, response.status_code)
    return response


app.include_router(auth_router)
app.include_router(user_router)


@app.get(
    "/hello",
    tags=["Test"],
    summary="Hello endpoint",
    description="Returns a hello message. Triggered by the Hello button on the frontend.",
)
async def hello():
    payload = {"message": "Hello"}
    logger.info("[GET] /hello → %s", payload)
    return payload
