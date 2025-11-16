from fastapi import HTTPException, UploadFile
from model.user import user_model
from datetime import datetime
import uuid
from pathlib import Path

PROFILE_DIR = Path("uploads/profile_images")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

class AuthController:

    ## 비밀번호 유효성 검증
    @staticmethod
    def validate_password(password: str):

        if not any(c.isupper() for c in password):
            raise HTTPException(400, "비밀번호에 대문자가 최소 1개 포함되어야 합니다.")
        if not any(c.islower() for c in password):
            raise HTTPException(400, "비밀번호에 소문자가 최소 1개 포함되어야 합니다.")
        if not any(c.isdigit() for c in password):
            raise HTTPException(400, "비밀번호에 숫자가 최소 1개 포함되어야 합니다.")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            raise HTTPException(400, "비밀번호에 특수문자가 최소 1개 포함되어야 합니다.")
    
    ## 프로필 이미지 저장
    @staticmethod
    async def save_profile_image(profile_image: UploadFile) -> str:
        if not profile_image or not profile_image.filename:
            return "/static/profile_images/default.jpg"
        
        if not profile_image.filename.lower().endswith('.jpg'):
            raise HTTPException(400, "프로필 사진은 .jpg 파일만 가능합니다")
        
        if profile_image.content_type != "image/jpeg":
            raise HTTPException(400, "JPEG 이미지만 업로드 가능합니다")
        
        contents = await profile_image.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(400, "파일 크기는 5MB 이하여야 합니다.")
        
        unique_filename = f"{uuid.uuid4().hex}.jpg"
        file_path = PROFILE_DIR / unique_filename
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return f"/static/profile_images/{unique_filename}"
    
    ## 회원가입
    @staticmethod
    async def signup(email: str, password: str, password_confirm: str, 
                     nickname: str, profile_image: UploadFile = None):
        # 이메일 중복 체크
        if user_model.find_by_email(email):
            raise HTTPException(400, "이미 사용중인 이메일입니다.")
        
        # 닉네임 중복 체크
        if user_model.find_by_nickname(nickname):
            raise HTTPException(400, "이미 사용중인 닉네임입니다.")
        
        # 비밀번호 유효성 체크
        AuthController.validate_password(password)
        
        if password != password_confirm:
            raise HTTPException(400, "비밀번호가 일치하지 않습니다.")
        
        # 프로필 이미지 저장
        profile_image_url = await AuthController.save_profile_image(profile_image)
        
        # 사용자 생성
        new_user = user_model.create({
            "email": email,
            "password": user_model.hash_password(password),
            "nickname": nickname,
            "profile_image_url": profile_image_url,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "id": new_user["id"],
            "email": new_user["email"],
            "nickname": new_user["nickname"],
            "profile_image_url": new_user["profile_image_url"]
        }
    
    ## 로그인
    @staticmethod
    def signin(email: str, password: str):

        # 사용자 찾기
        user = user_model.find_by_email(email)
        if not user:
            raise HTTPException(401, "이메일 또는 비밀번호가 잘못되었습니다.")
        
        # 비밀번호 확인
        if user['password'] != user_model.hash_password(password):
            raise HTTPException(401, "이메일 또는 비밀번호가 잘못되었습니다.")
        
        return {
            "id": user["id"],
            "email": user["email"],
            "nickname": user["nickname"],
            "profile_image_url": user["profile_image_url"]
        }

auth_controller = AuthController()