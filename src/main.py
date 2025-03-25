from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.admin.views import PostAdmin, UserAdmin, WorkoutAdmin
from src.database import engine
from src.auth2.router import router as auth_router

from src.users.router import user_router
from src.workout.router import router as workout_router
from src.posts.router import router as post_router
from src.dev_app.router import router as dev_router
from src.tasks.router import router as task_router
from src.community.router import router as comm_router
from src.achievements.router import router as achievement_router
from src.messages.router import router as message_router


from src.pages.task_router import router as page_task_router
from src.pages.post_router import router as page_post_router
from src.pages.user_router import router as page_user_router
from src.pages.main_router import router as main_router
from src.pages.dev_router import router as page_dev_router
from src.pages.community_router import router as page_comm_router
from src.pages.workout_router import router as page_workout_router

version = "v1"

description = """
A REST API for a Social Network.

This REST API is able to;
- Create Read Update And delete Posts
    """

version_prefix = f"/api/{version}"


app = FastAPI(
    title="Pet Social Network",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Evgeniy Reshetov",
        "url": "https://github.com/Ridmovies",
    },
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Подключение админки
admin = Admin(app, engine)
admin.add_view(PostAdmin)
admin.add_view(UserAdmin)
admin.add_view(WorkoutAdmin)

# Маршруты для API
app.include_router(auth_router, prefix=version_prefix)
app.include_router(user_router, prefix=version_prefix)
app.include_router(workout_router, prefix=version_prefix)
app.include_router(post_router, prefix=version_prefix)
app.include_router(dev_router, prefix=version_prefix)
app.include_router(task_router, prefix=version_prefix)
app.include_router(comm_router, prefix=version_prefix)
app.include_router(achievement_router, prefix=version_prefix)
app.include_router(message_router, prefix=version_prefix)


# Маршруты для страниц
app.include_router(main_router)
app.include_router(page_post_router)
app.include_router(page_user_router)
app.include_router(page_task_router)
app.include_router(page_dev_router)
app.include_router(page_comm_router)
app.include_router(page_workout_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

