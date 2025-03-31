from fastapi import APIRouter, Depends, Request

from src.auth2.jwt_utils import UserDep
from src.events.router import get_all_events, get_event_details
from src.templates import templates


router = APIRouter(prefix="/events", tags=["page_events"])


@router.get("")
async def get_all_events_page(
        request: Request,
        events=Depends(get_all_events)
):
    return templates.TemplateResponse(
        name="events/event_list.html",
        context={"request": request, "events": events},
    )


@router.get("/create")
async def create_event_page(
    request: Request,
    user: UserDep,
):
    return templates.TemplateResponse(
        name="events/create_event.html",
        context={"request": request, "user": user},
    )


@router.get("/{event_id}")
async def event_details_page(
        request: Request,
        user: UserDep,
        event=Depends(get_event_details)
):
    return templates.TemplateResponse(
        name="events/event_detail.html",
        context={"request": request, "user": user, "event": event},
    )