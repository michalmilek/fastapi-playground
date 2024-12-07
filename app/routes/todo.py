from ..schemas import TodoBaseSchema
from ..models import todo as todo_model
from ..schemas import ListTodoResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..config.database import get_db

router = APIRouter()


@router.get('/')
def get_todos(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    todos = db.query(todo_model.Todo).filter(
        todo_model.Todo.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(todos), 'todos': todos}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoBaseSchema, db: Session = Depends(get_db)):
    new_todo = todo_model.Todo(**payload.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"status": "success", "todo": new_todo}


@router.patch('/{todoId}')
def update_todo(todoId: str, payload: TodoBaseSchema, db: Session = Depends(get_db)):
    todo_query = db.query(todo_model.Todo).filter(todo_model.Todo.id == todoId)
    db_todo = todo_query.first()

    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No todo with this id: {todoId} found')
    update_data = payload.model_dump(exclude_unset=True)
    todo_query.filter(todo_model.Todo.id == todoId).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_todo)
    return {"status": "success", "todo": db_todo}


@router.get('/{todoId}')
def get_todo(todoId: str, db: Session = Depends(get_db)):
    todo = db.query(todo_model.Todo).filter(todo_model.Todo.id == todoId).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No todo with this id: {id} found")
    return {"status": "success", "todo": todo}


@router.delete('/{todoId}')
def delete_todo(todoId: str, db: Session = Depends(get_db)):
    todo_query = db.query(todo_model.Todo).filter(todo_model.Todo.id == todoId)
    todo = todo_query.first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No todo with this id: {id} found')
    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)