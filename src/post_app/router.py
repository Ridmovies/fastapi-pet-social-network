from fastapi import APIRouter

router = APIRouter(prefix="/post", tags=["post"])

@router.get("")
async def root():
    return {"message": "Hello World"}

