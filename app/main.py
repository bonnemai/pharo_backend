import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware import Middleware

from .api.routes import router as api_router

allow_origin = os.environ.get("ALLOW_ORIGIN", "*")

middleware = [
    Middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=[allow_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

FAVICON_PATH = Path(__file__).resolve().parent / "resources" / "favicon.svg"

app.include_router(api_router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(FAVICON_PATH, media_type="image/svg+xml")


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI REST API!"}
