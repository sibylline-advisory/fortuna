import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..dependency.db import get_db_session, DBSession, safe_db_read, safe_db_write
from ..model.orm import Task
from ..model.request import CreateTaskPayload

log = logging.getLogger(__name__)
router = APIRouter(
    prefix="/v1/task",
    tags=["Task"]
)


@router.post('/')
async def create_task(payload: CreateTaskPayload,
                      db: DBSession = Depends(get_db_session)):
    task = Task(
        type=payload.type,
        text=payload.text,
        user_id="example user id",  # TODO: replace with actual user id
    )
    safe_db_write([task], db)
    return {"tid": task.tid}
