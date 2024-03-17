import time
from typing import List

import requests
from sqlmodel import select

from api.api.dependency import get_db_session, safe_db_read
from api.api.model.orm import Task


def main():
    db = next(get_db_session())
    while True:
        time.sleep(1)
        tasks: List[Task] = safe_db_read(select(Task).where(Task.status == "pending"), db, one=False)
        print(tasks)
        for task in tasks:
            print(f"Processing task: {task.tid}")
            requests.post("http://localhost:8000/v1/task/resolver", json={
                "tid": task.tid,
            })


if __name__ == "__main__":
    main()
