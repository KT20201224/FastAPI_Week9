from fastapi import APIRouter, Form, File, UploadFile
from controller.user_controller import user_controller

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user": user_controller.get_user(user_id)}

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    nickname: str = Form(None, max_length=10),
    password: str = Form(None, min_length=8, max_length=20),
    profile_image: UploadFile = File(None)
):
    user = await user_controller.update_user(user_id, nickname, password, profile_image)
    return {
        "message": "회원정보가 수정되었습니다.",
        "user": user
    }