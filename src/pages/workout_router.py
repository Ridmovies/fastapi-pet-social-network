from fastapi import APIRouter, Depends, Request

from src.auth2.jwt_utils import UserDep
from src.templates import templates
from src.workout.router import get_user_workout

router = APIRouter(prefix="/workouts", tags=["page_workouts"])


@router.get("")
async def get_user_workouts_page(
        request: Request,
        user: UserDep,
        workouts=Depends(get_user_workout)
):
    return templates.TemplateResponse(
        name="workouts/workout_list.html",
        context={"request": request, "user": user, "workouts": workouts},
    )
