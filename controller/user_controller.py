from fastapi import HTTPException, UploadFile
from model.user import user_model
from controller.auth_controller import AuthController

class UserController:

    ## 회원정보 수정
    @staticmethod
    async def update_user(user_id: int, nickname: str = None, 
                          password: str = None, profile_image: UploadFile = None):
        
        # 사용자 찾기
        user = user_model.find_by_id(user_id)
        if not user:
            raise HTTPException(404, "사용자를 찾을 수 없습니다.")
        
        updates = {}
        
        # 닉네임 수정
        if nickname is not None:
            if not nickname.strip():
                raise HTTPException(400, "닉네임을 입력해주세요.")
            if len(nickname) > 10:
                raise HTTPException(400, "닉네임은 10자 이하여야 합니다.")
            
            # 닉네임 중복 체크 (자신 제외)
            existing = user_model.find_by_nickname(nickname)
            if existing and existing['id'] != user_id:
                raise HTTPException(400, "이미 사용중인 닉네임입니다.")
            
            updates["nickname"] = nickname
        
        # 비밀번호 수정
        if password is not None:
            AuthController.validate_password(password)
            updates["password"] = user_model.hash_password(password)
        
        # 프로필 이미지 수정
        if profile_image:
            profile_image_url = await AuthController.save_profile_image(profile_image)
            updates["profile_image_url"] = profile_image_url
        
        # 업데이트
        if updates:
            updated_user = user_model.update(user_id, updates)
        else:
            updated_user = user
        
        return {
            "id": updated_user["id"],
            "email": updated_user["email"],
            "nickname": updated_user["nickname"],
            "profile_image_url": updated_user["profile_image_url"]
        }
    
    ## 사용자 정보 조회
    @staticmethod
    def get_user(user_id: int):
        """사용자 정보 조회"""
        user = user_model.find_by_id(user_id)
        if not user:
            raise HTTPException(404, "사용자를 찾을 수 없습니다.")
        
        return {
            "id": user["id"],
            "email": user["email"],
            "nickname": user["nickname"],
            "profile_image_url": user["profile_image_url"],
            "created_at": user.get("created_at")
        }

user_controller = UserController()