from app.models import note as note_model
from app.models import todo as todo_model
from app.models import user as user_model
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import note, todo, user, auth
from app.config.database import engine

note_model.Base.metadata.create_all(bind=engine)
todo_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note.router, tags=['Notes'], prefix='/api/notes')
app.include_router(todo.router, tags=['Todos'], prefix='/api/todos')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
