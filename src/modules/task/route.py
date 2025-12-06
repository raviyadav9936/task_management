from fastapi import APIRouter,Depends
from database.database import get_db
from sqlalchemy.orm import Session
from modules.task.crud import create_task,update_task,delete_task,get_all_tasks,get_task_by_id
from modules.task.schema import TaskCreateSchema,TaskOut
from modules.auth.oauth import get_current_user


router=APIRouter()


@router.post("/")
def add_task(schema: TaskCreateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_task(db, schema, current_user)


@router.get("/")
def list_all_tasks(db: Session = Depends(get_db)):
    return get_all_tasks(db)


@router.get("/{task_id}")
def task_detail(task_id: int, db: Session = Depends(get_db)):
    return get_task_by_id(db, task_id)


@router.put("/{task_id}")
def task_update(task_id: int, schema: TaskCreateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_task(db, task_id, schema, current_user)


@router.delete("/{task_id}")
def task_delete(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_task(db, task_id, current_user)



