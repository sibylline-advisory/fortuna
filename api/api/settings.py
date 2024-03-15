import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    test_mode: bool = os.environ.get("IS_TEST_MODE", True)
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")


settings = Settings()
