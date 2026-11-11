from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from models.user import User
from schemas.tasks import TaskCreate, TaskUpdate, TaskStatusUpdate
from dependencies import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# 创建任务
@router.post("/", status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# 查询当前用户的所有任务
@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).all()

    return tasks


# 查询单个任务
@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# 更新任务
@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description

    db.commit()
    db.refresh(task)

    return task


# 删除任务
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()


# 修改任务完成状态
@router.patch("/{task_id}/status")
def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = status_update.completed

    db.commit()
    db.refresh(task)

    return task

