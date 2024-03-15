import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import routers
from .settings import settings, secure_settings

VERSION = "0.1.0"

logging.basicConfig(stream=sys.stdout, level=settings.log_level)
log = logging.getLogger(__name__)

app = FastAPI(
    title="Fortuna API",
    description="REST API for Fortuna",
    version=VERSION,
    docs_url="/hidden/docs",
    redoc_url="/hidden/redoc",
    openapi_url="/hidden/openapi.json"
)

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:4242",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    log.info(f"Starting Fortuna API service - version: {VERSION}")
    log.info(settings)
    if settings.test_mode:
        log.info("Running in test mode")
        log.info(secure_settings)
        from .dependency.db import make_migrations
        make_migrations()


for router in routers:
    app.include_router(router)


@app.get("/", name="Base", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    return {"msg": "ok"}
