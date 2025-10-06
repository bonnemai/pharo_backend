import json
import os
from datetime import datetime, timezone
from logging.config import dictConfig
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from mangum import Mangum
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware import Middleware

from .api.routes import router as api_router


LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()
LOGGING_CONFIG_PATH = Path(__file__).resolve().parent / "config" / "logging.json"

with LOGGING_CONFIG_PATH.open("r", encoding="utf-8") as config_file:
    logging_config = json.load(config_file)

logging_config["handlers"]["default"]["level"] = LOG_LEVEL
logging_config["root"]["level"] = LOG_LEVEL

dictConfig(logging_config)

allow_origins = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if o.strip()]
middleware = [
    Middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=allow_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

FAVICON_PATH = Path(__file__).resolve().parent / "resources" / "favicon.svg"
HOME_PAGE_PATH = Path(__file__).resolve().parent / "resources" / "home.html"
BUILD_DATE = os.environ.get("BUILD_DATE", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
HOME_PAGE_HTML = HOME_PAGE_PATH.read_text(encoding="utf-8").replace("{{BUILD_DATE}}", BUILD_DATE)

app.include_router(api_router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(FAVICON_PATH, media_type="image/svg+xml")


@app.get("/", response_class=HTMLResponse)
async def read_root() -> str:
    return HOME_PAGE_HTML


handler = Mangum(app, api_gateway_base_path="/", lifespan="auto")
