from fastapi import APIRouter, Form, File, UploadFile
from controller.auth_controller import auth_controller

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(
    email: str = Form(...),
    password: str = Form(..., min_length=8, max_length=20),
    password_confirm: str = Form(...),
    nickname: str = Form(..., max_length=10),
    profile_image: UploadFile = File(None)
):
    user = await auth_controller.signup(email, password, password_confirm, nickname, profile_image)
    return {
        "message": "회원가입이 완료되었습니다.",
        "user": user
    }

@router.post("/signin")
async def signin(
    email: str = Form(...),
    password: str = Form(..., min_length=8, max_length=20)
):
    user = auth_controller.signin(email, password)
    return {
        "message": "로그인 성공",
        "user": user
    }