from app.config.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from enum import Enum as PyEnum

class TodoCategory(PyEnum):
    WORK = "work"
    PERSONAL = "personal"
    SHOPPING = "shopping"
    OTHER = "other"

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(SQLAlchemyEnum(TodoCategory), nullable=True)
    done = Column(Boolean, nullable=False, default=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())