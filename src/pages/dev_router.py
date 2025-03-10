import markdown
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from src.dev_app.router import get_github_commits

router = APIRouter(prefix="/dev", tags=["page_dev"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/github-commits")
async def show_github_commits(request: Request):
    owner = "Ridmovies"  # Владелец репозитория
    repo = "fastapi-pet-social-network"  # Название репозитория
    commits = await get_github_commits(owner, repo)  # Получаем коммиты
    return templates.TemplateResponse(
        name="dev/github_commits.html",
        context={"request": request, "commits": commits},
    )


@router.get("/roadmap")
async def roadmap_view(request: Request):
    # Загружаем файл roadmap.md
    with open("src/dev_app/roadmap.md", "r") as f:
        content = f.read()

    # Преобразуем Markdown в HTML
    html_content = markdown.markdown(content)

    return templates.TemplateResponse(
        name="dev/roadmap.html",
        context={"request": request, "roadmap": html_content},
    )
