from datetime import datetime
from typing import List
from pydantic import BaseModel
from uuid import UUID


class NoteBaseSchema(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str | None = None
    published: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListNoteResponse(BaseModel):
    status: str
    results: int
    notes: List[NoteBaseSchema]

class TodoBaseSchema(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str | None = None
    published: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListTodoResponse(BaseModel):
    status: str
    results: int
    todos: List[TodoBaseSchema]
    
class UserBaseSchema(BaseModel):
    id: UUID | None = None
    email: str
    password: str
    refreshTokens: List[str] | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        from_attributes = True

class UserRegisterSchema(BaseModel):
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str