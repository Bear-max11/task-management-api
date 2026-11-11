from database import engine, Base
from models import task, user

from routers.tasks import router as tasks_router
from fastapi import FastAPI
from routers.users import router as users_router
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(tasks_router)
app.include_router(users_router)
@app.get("/")
def root():
	return {"message": "Task Management API"}

