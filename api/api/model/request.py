from pydantic import BaseModel

from ..model.enum import TaskType


class CreateTaskPayload(BaseModel):
    type: TaskType
    text: str


class ResolverPayload(BaseModel):
    tid: str


class AckTask(BaseModel):
    op_hash: str
