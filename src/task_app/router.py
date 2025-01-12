from fastapi import APIRouter
from sqlalchemy import desc

from src.auth_app.dependencies import UserDep
from src.task_app.models import Task
from src.task_app.schemas import TaskSchema
from src.task_app.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def get_all_tasks(user: UserDep):
    return await TaskService.get_all(order_by=desc(Task.created_at), user_id=user.id)


@router.post("")
async def create_task(user: UserDep, task_data: TaskSchema):
    return await TaskService.create_task(user.id, task_data)


@router.get("/{task_id}/complete")
async def complete_task(user: UserDep, task_id: int):
    return await TaskService.completed_task(task_id, user.id)


@router.delete("/{task_id}")
async def delete_task(user: UserDep, task_id: int):
    return await TaskService.delete_task(task_id, user.id)