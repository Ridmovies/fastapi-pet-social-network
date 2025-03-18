from fastapi import APIRouter, Depends, Request

from src.auth.dependencies import UserDep
from src.community.router import get_all_communities
from src.templates import templates

router = APIRouter(prefix="/community", tags=["page_community"])


@router.get("")
async def get_communities_page(
        request: Request,
        user: UserDep,
        communities=Depends(get_all_communities)):
    return templates.TemplateResponse(
        name="community/community_list.html",
        context={"request": request, "user": user, "communities": communities},
    )