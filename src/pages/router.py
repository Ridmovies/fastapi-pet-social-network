from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse

from src.post_app.router import get_all_posts
from src.task_app.router import get_all_tasks
from src.task_app.service import TaskService

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/tasks")
async def get_tasks_page(
        request: Request,
        tasks=Depends(get_all_tasks),
):
    return templates.TemplateResponse(
        name="tasks.html",
        context={"request": request, "tasks": tasks},
    )
#
@router.get("/{task_id}/complete/")
async def page_complete_task(task_id: int):
    await TaskService.completed_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)


@router.get("/{task_id}")
async def page_delete_task(task_id: int):
    await TaskService.delete(task_id)
    return RedirectResponse(url="/tasks", status_code=303)

@router.get("/posts")
async def get_posts_page(
    request: Request,
    posts=Depends(get_all_posts),
):
    return templates.TemplateResponse(
        name="posts.html",
        context={"request": request, "posts": posts},
    )





# @app.get("/")
# async def root(request: Request):
#     task_id = 123  # пример id задачи
#     link_to_completed_task = request.url_for("completed_task", task_id=task_id)
#
#     return {
#         "link_to_completed_task": link_to_completed_task,
#         "message": "This is a test message."
#     }