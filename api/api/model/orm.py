import time
from typing import Optional, List
import uuid

from sqlalchemy import TEXT, Column, BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import SQLModel, Field, Relationship

from .enum import *


class User(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    created_at: int = Field(sa_column=Column(BigInteger()), default_factory=lambda: time.time() * 1000)
    tasks: Optional[List["Task"]] = Relationship(
        back_populates="user",
        sa_relationship=RelationshipProperty(
            "Task",
            primaryjoin="foreign(User.uid) == Task.user_id",
            uselist=True,
            viewonly=False
        )
    )


class Task(SQLModel, table=True):
    tid: str = Field(primary_key=True, default_factory=lambda: f"tid-{uuid.uuid4().hex}")
    created_at: int = Field(sa_column=Column(BigInteger()), default_factory=lambda: time.time() * 1000)
    type: TaskType
    text: str
    user_id: str = Field(index=True)
    user: User = Relationship(
        back_populates="tasks",
        sa_relationship=RelationshipProperty(
            "User",
            primaryjoin="foreign(Task.user_id) == User.uid",
            uselist=False,
            viewonly=True
        )
    )
    status: Optional[str]
    call_data: Optional[str] = Field(sa_column=Column(LONGTEXT))
