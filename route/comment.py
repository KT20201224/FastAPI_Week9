from fastapi import APIRouter, Form
from controller.comment_controller import comment_controller

router = APIRouter(prefix="/posts", tags=["comments"])

@router.post("/{post_id}/comments")
async def create_comment(
    post_id: int,
    user_id: int = Form(...),
    content: str = Form(...)
):
    comment = comment_controller.create_comment(post_id, user_id, content)
    return {
        "message": "댓글이 등록되었습니다.",
        "comment": comment
    }

@router.get("/{post_id}/comments")
async def get_comments(post_id: int):
    return comment_controller.get_comments(post_id)

@router.put("/comments/{comment_id}")
async def update_comment(
    comment_id: int,
    user_id: int = Form(...),
    content: str = Form(...)
):
    comment = comment_controller.update_comment(comment_id, user_id, content)
    return {
        "message": "댓글이 수정되었습니다.",
        "comment": comment
    }

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: int = Form(...)
):
    return comment_controller.delete_comment(comment_id, user_id)