from fastapi import APIRouter, Depends, Request

from src.auth.dependencies import UserDep
from src.community.router import get_all_communities, get_community_details
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

@router.get("/{community_id}")
async def get_community_details_page(
    request: Request,
    user: UserDep,
    community=Depends(get_community_details),
):
    return templates.TemplateResponse(
        name="community/community_detail.html",
        context={"request": request, "community": community, "user": user},
    )
