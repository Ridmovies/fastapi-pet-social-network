from src.database import async_session
from src.services import BaseService
from src.task_app.models import Task


class TaskService(BaseService):
    model = Task


    @classmethod
    async def completed_task(cls, task_id):
        async with async_session() as session:
            task = await session.get(Task, task_id)
            if task.completed is False:
                task.completed = True
            else:
                task.completed = False
            await session.commit()
            return task



