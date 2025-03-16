from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, JSONResponse

from src.pages.forms import TaskForm
from src.tasks.router import get_all_tasks
from src.tasks.service import TaskService

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


@router.get("/{task_id}/complete")
async def page_complete_task(task_id: int):
    await TaskService.completed_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)


@router.delete("/{task_id}")
async def page_delete_task(task_id: int):
    await TaskService.delete(task_id)
    return JSONResponse({"message": f"Task {task_id} успешно удален."})


@router.get("/add")
async def show_form(
    request: Request,
):
    form = TaskForm
    return templates.TemplateResponse(
        name="add_task.html",
        context={"request": request, "form": form},
    )


@router.post("/add")
async def handle_form(
    request: Request,
    title: str = Form(...),
    description: str | None = Form(None),
    completed: bool = Form(False),
    priority: str = Form("Low"),
):
    form_data = TaskForm(
        title=title, description=description, completed=completed, priority=priority
    )
    await TaskService.create(form_data)
    return RedirectResponse(url="/tasks", status_code=303)
    # return RedirectResponse(url=request.url_for("show_form"), status_code=303)
