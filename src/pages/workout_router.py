from fastapi import APIRouter, Depends, Request

from src.auth2.jwt_utils import UserDep
from src.templates import templates
from src.workout.router import get_user_workout, get_user_workout_statistics, workout_details

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


@router.get("/statistics")
async def get_user_workout_statistics_page(
        request: Request,
        user: UserDep,
        stats=Depends(get_user_workout_statistics)
):
    return templates.TemplateResponse(
        name="workouts/workout_stat.html",
        context={"request": request, "user": user, "stats": stats},
    )

@router.get("/upload")
async def get_upload_workout_page(
        request: Request,
        user: UserDep,
):
    return templates.TemplateResponse(
        name="workouts/workout_upload.html",
        context={"request": request, "user": user},
    )

@router.get("/{workout_id}")
async def workout_details_page(
        request: Request,
        user: UserDep,
        workout=Depends(workout_details)
):
    return templates.TemplateResponse(
        name="workouts/workout_detail.html",
        context={"request": request, "user": user, "workout": workout},
    )