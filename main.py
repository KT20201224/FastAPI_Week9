from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from route import auth, post, user, comment

app = FastAPI(title="Community API", version="1.0.0")

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# 라우터 등록
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)

@app.get("/")
async def root():
    return {
        "message": "Community API Server",
        "version": "1.0.0",
        "docs": "/docs"
    }