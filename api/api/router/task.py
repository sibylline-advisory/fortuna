import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..dependency import get_user
from ..dependency.db import get_db_session, DBSession, safe_db_read, safe_db_write
from ..model.orm import Task, User
from ..model.request import CreateTaskPayload

log = logging.getLogger(__name__)
router = APIRouter(
    prefix="/v1/task",
    tags=["Task"]
)


@router.post('/')
async def create_task(payload: CreateTaskPayload,
                      user: User = Depends(get_user),
                      db: DBSession = Depends(get_db_session)):
    task = Task(
        **payload.dict(),
        user_id=user.uid
    )
    safe_db_write([task], db)
    return {"tid": task.tid}
