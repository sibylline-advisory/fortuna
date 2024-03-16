import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..dependency import get_user
from ..dependency.db import get_db_session, DBSession, safe_db_read, safe_db_write
from ..llama.task import get_chat_agent
from ..model.orm import Task, User
from ..model.request import CreateTaskPayload, ResolverPayload, AckTask

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


@router.post("/resolver")
async def resolve_task(payload: ResolverPayload,
                       db: DBSession = Depends(get_db_session)):
    log.info("Resolving task with payload: %s", payload.dict())
    pending_task: Task = safe_db_read(select(Task).where(Task.tid == payload.tid), db)
    log.info("Got pending task: %s", pending_task.dict())
    resolver_agent = get_chat_agent()
    resolver_agent.chat(pending_task.text)

    return {}


@router.get("/{tid}")
async def get_task(tid: int,
                   db: DBSession = Depends(get_db_session)):
    task = safe_db_read(select(Task).where(Task.tid == tid), db)
    return task


@router.patch("/{tid}")
async def update_task(tid: int,
                      payload: AckTask,
                      db: DBSession = Depends(get_db_session)):
    task = safe_db_read(select(Task).where(Task.tid == tid), db)
    for key, value in payload.dict().items():
        setattr(task, key, value)
    safe_db_write([task], db)
    return task