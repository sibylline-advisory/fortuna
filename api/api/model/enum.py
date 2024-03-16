from enum import Enum


class TaskType(str, Enum):
    intent = "intent"
    spot = "spot"
