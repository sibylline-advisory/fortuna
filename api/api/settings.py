import logging
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    test_mode: bool = os.environ.get("IS_TEST_MODE", True)
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")

    db_user: str = os.environ.get("DB_USER", "8lb9rk034pk6lyeokjrq")
    db_host: str = os.environ.get("DB_HOST", "gcp.connect.psdb.cloud")
    db_port: str = os.environ.get("DB_PORT", "3306")
    db_handler: str = os.environ.get("DB_HANDLER", "mysql+mysqldb")
    db_name: str = os.environ.get("DB_NAME", "fortuna")


class SecureSettings(BaseSettings):
    db_password: str = os.environ.get(
        "DB_PASSWORD", "pscale_pw_cqKV7uLebQ62W0WcfWsCB86HPG6xt6xqhtx43vULOCz")
    openai_key: str = os.environ.get("OPENAI_API_KEY", "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")


settings = Settings()
secure_settings = SecureSettings()

if settings.test_mode:
    settings.log_level = "DEBUG"
    logging.getLogger("httpcore").setLevel("INFO")
