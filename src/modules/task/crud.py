from database.models import User
from fastapi import HTTPException
from database.models import Task

# Task CRUD
def create_task(db, schema, user: User):
    try:
        task = Task(
            title=schema.title,
            description=schema.description,
            completed=schema.completed,
            user_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        return{
            'status':True,
            'message':'Task created successfully',
            'data':{
                'title':task.title,
                'description':task.description,
                'completed':task.completed,
                'user_id':task.user_id
            }
        }
        return task
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'something went wrogn'}


def get_all_tasks(db):
    try:
        fetch_task= db.query(Task).all()

        tasks=[
            {
                'id':item.id,
                'title':item.title,
                'description':item.description,
                'completed':item.completed,
                'user_id':item.user_id,
                'created_at':item.created_at,
                'updated_at':item.updated_at
            }
            for item in fetch_task
        ]

        return {
            'status':True,
            'message':'Task fetch successfully',
            'data':tasks
        }
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}    
        

def get_task_by_id(db, task_id: int):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        result={
            'id':task.id,
            'title':task.title,
            'description':task.description,
            'completed':task.completed,
            'user_id':task.user_id,
            'created_at':task.created_at,
            'updated_at':task.updated_at
        }

        return {
            'status':True,
            'message':'Fetch task successfully',
            'data':result
        }
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}    
        

def update_task(db, task_id: int, schema, user):
    try:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or not allowed")
        
        task.title = schema.title
        task.description = schema.description
        task.completed = schema.completed
        db.commit()
        db.refresh(task)

        return {
            'status':True,
            'message':'Task updated successfully'
        }
        # return task

    except HTTPException as e:
        raise e
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}    
        

def delete_task(db, task_id: int, user):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or not allowed")
        db.delete(task)
        db.commit()
        return {"detail": "Task deleted successfully"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print('error',e)
        return {'status':False,'message':'Something went wrogn'}    
        









