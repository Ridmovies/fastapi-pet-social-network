from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, JSONResponse

from src.task_app.router import get_all_tasks
from src.task_app.service import TaskService

router = APIRouter(prefix="/tasks", tags=["page_tasks"])
templates = Jinja2Templates(directory="src/templates")


@router.get("")
async def get_tasks_page(
        request: Request,
        tasks=Depends(get_all_tasks),
):
    return templates.TemplateResponse(
        name="tasks.html",
        context={"request": request, "tasks": tasks},
    )
#
@router.get("/{task_id}/complete")
async def page_complete_task(task_id: int):
    await TaskService.completed_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)


@router.delete("/{task_id}")
async def page_delete_task(task_id: int):
    await TaskService.delete(task_id)
    return JSONResponse({"message": f"Task {task_id} успешно удален."})



