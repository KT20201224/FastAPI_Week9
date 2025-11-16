from fastapi import HTTPException
from model.comment import comment_model
from model.user import user_model
from model.post import post_model
from datetime import datetime

class CommentController:

    ## 댓글 작성
    @staticmethod
    def create_comment(post_id: int, user_id: int, content: str):
        # 게시글 확인
        post = post_model.find_by_id(post_id)
        if not post:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
        
        # 사용자 확인
        user = user_model.find_by_id(user_id)
        if not user:
            raise HTTPException(404, "사용자를 찾을 수 없습니다.")
        
        # 내용 검증
        if not content.strip():
            raise HTTPException(400, "댓글 내용을 입력해주세요.")
        
        # 댓글 생성
        now = datetime.now().isoformat()
        new_comment = comment_model.create({
            "post_id": post_id,
            "user_id": user_id,
            "author_nickname": user["nickname"],
            "author_profile_image": user["profile_image_url"],
            "content": content,
            "created_at": now,
            "updated_at": now
        })
        
        # 게시글의 댓글 수 업데이트
        comment_count = comment_model.count_by_post_id(post_id)
        post_model.update(post_id, {"comments_count": comment_count})
        
        return new_comment
    

    ## 댓글 목록 조회
    @staticmethod
    def get_comments(post_id: int):
        # 게시글 확인
        post = post_model.find_by_id(post_id)
        if not post:
            raise HTTPException(404, "게시글을 찾을 수 없습니다.")
        
        comments = comment_model.find_by_post_id(post_id)
        return {
            "total": len(comments),
            "comments": comments
        }
    
    ## 댓글 수정
    @staticmethod
    def update_comment(comment_id: int, user_id: int, content: str):
        # 댓글 찾기
        comment = comment_model.find_by_id(comment_id)
        if not comment:
            raise HTTPException(404, "댓글을 찾을 수 없습니다.")
        
        # 작성자 확인
        if comment['user_id'] != user_id:
            raise HTTPException(403, "수정 권한이 없습니다.")
        
        # 내용 검증
        if not content.strip():
            raise HTTPException(400, "댓글 내용을 입력해주세요.")
        
        # 수정
        updated_comment = comment_model.update(comment_id, {
            "content": content,
            "updated_at": datetime.now().isoformat()
        })
        
        return updated_comment
    
    ## 댓글 삭제
    @staticmethod
    def delete_comment(comment_id: int, user_id: int):
        # 댓글 찾기
        comment = comment_model.find_by_id(comment_id)
        if not comment:
            raise HTTPException(404, "댓글을 찾을 수 없습니다.")
        
        # 작성자 확인
        if comment['user_id'] != user_id:
            raise HTTPException(403, "삭제 권한이 없습니다.")
        
        post_id = comment['post_id']
        
        # 삭제
        success = comment_model.delete(comment_id)
        if not success:
            raise HTTPException(500, "댓글 삭제에 실패했습니다.")
        
        # 게시글의 댓글 수 업데이트
        comment_count = comment_model.count_by_post_id(post_id)
        post_model.update(post_id, {"comments_count": comment_count})
        
        return {"message": "댓글이 삭제되었습니다."}

comment_controller = CommentController()