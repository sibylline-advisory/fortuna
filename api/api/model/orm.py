from typing import Optional, List
import uuid

from sqlalchemy.orm import RelationshipProperty
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(
        back_populates="user",
        sa_relationship=RelationshipProperty(
            "Request",
            primaryjoin="foreign(User.uid) == Task.user_id",
            uselist=True,
            viewonly=False
        )
    )


class Task(SQLModel, table=True):
    tid: str = Field(primary_key=True, default_factory=lambda: f"tid-{uuid.uuid4().hex}")
    type: str
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
