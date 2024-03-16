import logging

import json

from sqlmodel import select

from ...dependency.db import refresh_db_session_mid_agent_call, safe_db_read, safe_db_write
from ...model.orm import Task

log = logging.getLogger(__name__)


def update_task_with_resolution(tid: str, call_data: dict) -> None:
    """Update the task with the resolution."""
    log.info(f"Updating task {tid} with resolution {call_data}")
    db = refresh_db_session_mid_agent_call()
    task: Task = safe_db_read(select(Task).where(Task.tid == tid), db)
    task.call_data = json.dumps(call_data)
    task.status = "resolved"
    safe_db_write([task], db)
    log.info(f"Updated task {tid} with resolution {call_data}")
