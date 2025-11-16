from fastapi import HTTPException, UploadFile
from model.post import post_model
from model.user import user_model
from datetime import datetime
import uuid
from pathlib import Path

POST_IMAGES_DIR = Path("uploads/post_images")
POST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

class PostController:

    ## 게시글 사진 저장
    @staticmethod
    async def save_post_image(image: UploadFile) -> str:
        if not image or not image.filename:
            return None
        
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        file_ext = Path(image.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(400, "이미지는 .jpg, .jpeg, .png 파일만 가능합니다.")
        
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(400, "JPEG 또는 PNG 이미지만 업로드 가능합니다.")
        
        contents = await image.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, "파일 크기는 10MB 이하여야 합니다.")
        
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = POST_IMAGES_DIR / unique_filename
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return f"/static/post_images/{unique_filename}"
    
    ## 게시글 등록
    @staticmethod
    async def create_post(title: str, content: str, user_id: int, image: UploadFile = None):
        # 사용자 확인
        user = user_model.find_by_id(user_id)
        if not user:
            raise HTTPException(404, "사용자를 찾을 수 없습니다.")
        
        # 유효성 검증
        if not title.strip():
            raise HTTPException(400, "제목을 입력해주세요.")
        if not content.strip():
            raise HTTPException(400, "내용을 입력해주세요.")
        if len(title) > 26:
            raise HTTPException(400, "제목은 26자 이하여야 합니다.")
        
        # 이미지 저장
        image_url = await PostController.save_post_image(image)
        
        # 게시글 생성
        now = datetime.now().isoformat()
        
        new_post = post_model.create({
            "title": title,
            "content": content,
            "image_url": image_url,
            "user_id": user_id,
            "author_nickname": user["nickname"],
            "author_profile_image": user["profile_image_url"],
            "created_at": now,
            "updated_at": now,
            "likes": 0,
            "comments_count": 0
        })
        
        return new_post
    

    # 게시글 수정
    @staticmethod
    async def update_post(post_id: int, user_id: int, title: str = None, 
                          content: str = None, image: UploadFile = None):

        # 게시글 찾기
        post = post_model.find_by_id(post_id)
        if not post:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
        
        # 작성자 확인
        if post['user_id'] != user_id:
            raise HTTPException(403, "수정 권한이 없습니다.")
        
        # 업데이트할 항목
        updates = {"updated_at": datetime.now().isoformat()}
        
        if title is not None:
            if not title.strip():
                raise HTTPException(400, "제목을 입력해주세요.")
            if len(title) > 26:
                raise HTTPException(400, "제목은 26자 이하여야 합니다.")
            updates["title"] = title
        
        if content is not None:
            if not content.strip():
                raise HTTPException(400, "내용을 입력해주세요.")
            updates["content"] = content
        
        if image:
            image_url = await PostController.save_post_image(image)
            updates["image_url"] = image_url
        
        # 업데이트
        updated_post = post_model.update(post_id, updates)
        return updated_post
    
    ## 게시글 목록 조회
    @staticmethod
    def get_posts(skip: int = 0, limit: int = 20):
        return post_model.find_all(skip, limit)
    
    ## 게시글 상세 조회
    @staticmethod
    def get_post(post_id: int):
        post = post_model.find_by_id(post_id)
        if not post:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
        return post
    
    ## 좋아요 추가/취소
    @staticmethod
    def toggle_like(post_id: int, user_id: int):
        from model.post import post_model
    
        post = post_model.find_by_id(post_id)
        if not post:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
    
        user = user_model.find_by_id(user_id)
        if not user:
            raise HTTPException(404, "사용자를 찾을 수 없습니다.")
    
        like_users = post.get('like_users', [])
    
        if user_id in like_users:
            # 좋아요 취소
            post_model.remove_like(post_id, user_id)
            return {"liked": False, "likes": len(like_users) - 1}
        else:
            # 좋아요 추가
            post_model.add_like(post_id, user_id)
            return {"liked": True, "likes": len(like_users) + 1}

    ## 조회수
    @staticmethod
    def increment_view(post_id: int):

        from model.post import post_model
    
        success = post_model.increment_view_count(post_id)
        if not success:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
    
        return {"message": "조회수가 증가했습니다."}

post_controller = PostController()