from fastapi import FastAPI
from database.database import Base,engine
import modules.task.route as task
import modules.auth.route as auth

Base.metadata.create_all(bind=engine)
app=FastAPI()


app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(task.router, tags=["Tasks"], prefix="/tasks")

