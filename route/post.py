from fastapi import APIRouter, Form, File, UploadFile
from controller.post_controller import post_controller

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("")
async def create_post(
    title: str = Form(..., max_length=26),
    content: str = Form(...),
    user_id: int = Form(...),
    image: UploadFile = File(None)
):
    post = await post_controller.create_post(title, content, user_id, image)
    return {
        "message": "게시글이 등록되었습니다.",
        "post": post
    }

@router.put("/{post_id}")
async def update_post(
    post_id: int,
    user_id: int = Form(...),
    title: str = Form(None, max_length=26),
    content: str = Form(None),
    image: UploadFile = File(None)
):
    post = await post_controller.update_post(post_id, user_id, title, content, image)
    return {
        "message": "게시글이 수정되었습니다.",
        "post": post
    }

@router.get("")
async def get_posts(skip: int = 0, limit: int = 20):
    return post_controller.get_posts(skip, limit)

@router.get("/{post_id}")
async def get_post(post_id: int):
    return {"post": post_controller.get_post(post_id)}

@router.post("/{post_id}/like")
async def toggle_like(
    post_id: int,
    user_id: int = Form(...)
):
    result = post_controller.toggle_like(post_id, user_id)
    return result

@router.post("/{post_id}/view")
async def increment_view(post_id: int):
    return post_controller.increment_view(post_id)

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user_id: int = Form(...)
):
    return post_controller.delete_post(post_id, user_id)