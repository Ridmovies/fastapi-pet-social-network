from src.database import async_session
from src.services import BaseService
from src.task_app.models import Task


class TaskService(BaseService):
    model = Task


    @classmethod
    async def completed_task(cls, task_id: int, user_id: int):
        async with async_session() as session:
            task: Task | None = await session.get(Task, task_id)
            if task.user_id == user_id:
                if task is not None:
                    if task.completed is False:
                        task.completed = True
                    else:
                        task.completed = False
                await session.commit()
                return task
            return {"message": "Task not found"}


    @classmethod
    async def create_task(cls, user_id, data):
        async with async_session() as session:
            data_dict = data.model_dump()
            instance = cls.model(**data_dict)
            instance.user_id = user_id
            session.add(instance)
            await session.commit()
            return instance


    @classmethod
    async def delete_task(cls, task_id: int, user_id: int):
        async with async_session() as session:
            task: Task | None = await session.get(Task, task_id)
            if task and task.user_id == user_id:
                await session.delete(task)
                await session.commit()
            return {"message": "Task not found"}

