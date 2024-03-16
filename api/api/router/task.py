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
    log.info(f"Resolving task with payload: {payload.dict()}")
    pending_task: Task = safe_db_read(select(Task).where(Task.tid == payload.tid), db)
    log.info(f"Got pending task: {pending_task.dict()}")
    resolver_agent = get_chat_agent()
    response = resolver_agent.chat(f"""
    We have received the following financial task (tid: {pending_task.tid}) from our client for you to resolve:
    
    {pending_task.text}
    
    Please resolve this task using the tools provided and update the task with the resolution in-line with our
    standards and expectations. Accuracy is essential due to the sensitivity and nature of our regulated
    financial offerings.
    
    When using each of the tools, ensure you call the tools correctly; directly with the required arguments and
    not wrapped in any other structure such as input.
    
    """)
    log.info(f"Got response from resolver agent: {response}")
    db.refresh(pending_task)
    log.info(pending_task)
    return pending_task.dict()


@router.get("/{tid}")
async def get_task(tid: str,
                   db: DBSession = Depends(get_db_session)):
    task = safe_db_read(select(Task).where(Task.tid == tid), db)
    return task


@router.patch("/{tid}")
async def update_task(tid: str,
                      payload: AckTask,
                      db: DBSession = Depends(get_db_session)):
    task = safe_db_read(select(Task).where(Task.tid == tid), db)
    for key, value in payload.dict().items():
        setattr(task, key, value)
    safe_db_write([task], db)
    return task