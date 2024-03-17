from enum import Enum


class TaskType(str, Enum):
    intent = "intent"
    spot = "spot"


class StatusType(str, Enum):
    pending = "pending"
    resolved = "resolved"
    acked = "acked"
