from fastapi import APIRouter
from sqlalchemy import desc

from src.auth.dependencies import UserDep
from src.database import SessionDep
from src.tasks.models import Task
from src.tasks.schemas import TaskSchema
from src.tasks.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def get_all_tasks(session: SessionDep, user: UserDep):
    return await TaskService.get_all(session, order_by=desc(Task.created_at), user_id=user.id)


# @router.post("")
# async def create_task(task_data: TaskSchema):
#     return await TaskService.create_task(user.id, task_data)


# @router.get("/{task_id}/complete")
# async def complete_task(user: UserDep, task_id: int):
#     return await TaskService.completed_task(task_id, user.id)
#
#
# @router.delete("/{task_id}")
# async def delete_task(user: UserDep, task_id: int):
#     return await TaskService.delete_task(task_id, user.id)