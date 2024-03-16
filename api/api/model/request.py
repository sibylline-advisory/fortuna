from pydantic import BaseModel

from ..model.enum import TaskType


class CreateTaskPayload(BaseModel):
    type: TaskType
    text: str
