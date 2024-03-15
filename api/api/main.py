import json
import logging
import sys
from fastapi import FastAPI, Request

from .settings import settings

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


@app.on_event("startup")
def on_startup():
    log.info(f"Starting API service - version: {VERSION}")
    log.info(json.dumps(
        settings.dict(),
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ))
    if settings.test_mode:
        log.info("Running in test mode")


@app.get("/", name="Base", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    return {"msg": "ok"}
