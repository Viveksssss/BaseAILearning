from fastapi import APIRouter

router = APIRouter(prefix="/usr", tags=["用户模块"])


@router.get("/list")
async def user_list():
    return {"data": ["user1", "user2"]}
