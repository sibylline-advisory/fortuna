import logging
import traceback
from functools import lru_cache
from tenacity import *
from typing import List, Optional

import sqlalchemy
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlmodel import Session as DBSession
from sqlmodel import create_engine, SQLModel

from ..errors import *
from ..settings import settings, secure_settings

log = logging.getLogger(__name__)


@lru_cache()
def get_engine():
    log.info(f"Connecting to DB: {settings.db_host} - {settings.db_name}")
    if secure_settings.db_password:
        connection_string = f"{settings.db_handler}://{settings.db_user}:{secure_settings.db_password}@" \
                            f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
    else:
        connection_string = f"{settings.db_handler}://{settings.db_user}@" \
                            f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
    return create_engine(connection_string,
                         pool_size=240,  # same as max concurrent requests. PS will LB this for free.
                         pool_recycle=3600,
                         pool_pre_ping=True,
                         max_overflow=128,
                         echo_pool=True,
                         isolation_level="AUTOCOMMIT",
                         connect_args={
                             "ssl": {
                                 "ssl_ca": "/etc/ssl/certs/ca-certificates.crt"
                             }
                         })


def make_migrations():
    log.info("Making migrations")
    SQLModel.metadata.create_all(get_engine())


def get_db_session():
    with DBSession(get_engine()) as db_session:
        try:
            yield db_session
        except sqlalchemy.exc.PendingRollbackError as rollback:
            log.warning(f"DB Needs to rollback")
            log.warning(rollback)
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=DATABASE_ERROR)
        except sqlalchemy.exc.OperationalError as e:
            log.warning(e)
            log.warning(traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=DATABASE_ERROR)


def safe_db_write(objects: List[BaseModel], db: DBSession):
    try:
        for obj in objects:
            log.debug(f"Adding object to txn: {obj}")
            db.add(obj)
        db.commit()
    except sqlalchemy.exc.IntegrityError as dupe:
        log.warning(dupe)
        log.warning(f"Shadow already exists.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=SHADOW_EXISTS)
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=DATABASE_ERROR)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1),
       retry=retry_if_exception_type(sqlalchemy.exc.OperationalError),
       reraise=True)
def safe_db_read(statement, db: DBSession, one: bool = True):
    try:
        if one:
            response = db.exec(statement).one()
        else:
            response = db.exec(statement).all()
        log.info(f"Returning item: {response}")
    except NoResultFound as none:
        log.warning(f"No results found for {str(statement)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except MultipleResultsFound as multiple:
        log.info(multiple)
        log.warning(f"Found multiple lines when 1 needed for {str(statement)}")
        return db.exec(statement).first()
    return response


def close_db_before_agent_call(db: DBSession, pre_commit_txn: Optional[List[SQLModel]] = None):
    log.info("Closing DB before agent call")
    if pre_commit_txn is not None:
        log.info(f"Pre-committing")
        safe_db_write(pre_commit_txn, db)
    db.close()


def refresh_db_session_mid_agent_call() -> DBSession:
    log.info("Refreshing DB session mid agent call")
    return next(get_db_session())
