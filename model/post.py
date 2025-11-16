import json
from pathlib import Path
from typing import List, Optional

class PostModel:
    def __init__(self):
        self.db_path = Path("data/posts.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    ## 모든 게시글 읽기
    def _read_all(self) -> List[dict]:
        if not self.db_path.exists():
            return []
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    ## 모든 게시글 쓰기
    def _write_all(self, posts: List[dict]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
    
    ## 다음 게시글 ID 생성
    def get_next_id(self) -> int:
        posts = self._read_all()
        if not posts:
            return 1
        return max(post["id"] for post in posts) + 1
    
    ## ID로 게시글 찾기
    def find_by_id(self, post_id: int) -> Optional[dict]:
        posts = self._read_all()
        return next((post for post in posts if post['id'] == post_id), None)
    
    ## 모든 게시글 조회(페이지네이션)
    def find_all(self, skip: int = 0, limit: int = 20) -> dict:
        posts = self._read_all()
        sorted_posts = sorted(posts, key=lambda x: x['created_at'], reverse=True)
        paginated = sorted_posts[skip:skip + limit]
        return {
            "total": len(posts),
            "posts": paginated
        }
    
    ## 사용자 ID로 특정 회원 게시글 검색
    def find_by_user_id(self, user_id: int) -> List[dict]:
        posts = self._read_all()
        return [post for post in posts if post['user_id'] == user_id]
    
    ## 게시글 생성
    def create(self, post_data: dict) -> dict:
        posts = self._read_all()
        post_data['id'] = self.get_next_id()
        posts.append(post_data)
        self._write_all(posts)
        return post_data
    
    ## 게시글 수정
    def update(self, post_id: int, updates: dict) -> Optional[dict]:
        posts = self._read_all()
        post = next((p for p in posts if p['id'] == post_id), None)
        if not post:
            return None
        post.update(updates)
        self._write_all(posts)
        return post
    
    ## 게시글 삭제
    def delete(self, post_id: int) -> bool:
        posts = self._read_all()
        original_length = len(posts)
        posts = [p for p in posts if p['id'] != post_id]
        if len(posts) < original_length:
            self._write_all(posts)
            return True
        return False
    
    ## 좋아요
    def add_like(self, post_id: int, user_id: int) -> bool:
        post = self.find_by_id(post_id)
        if not post:
            return False
    
        like_users = post.get('like_users', [])
        if user_id in like_users:
            return False  # 이미 좋아요 누름
    
        like_users.append(user_id)
        self.update(post_id, {
            'like_users': like_users,
            'likes': len(like_users)
        })
        return True

    ## 좋아요 취소
    def remove_like(self, post_id: int, user_id: int) -> bool:
        post = self.find_by_id(post_id)
        if not post:
            return False
    
        like_users = post.get('like_users', [])
        if user_id not in like_users:
            return False  # 좋아요 안 누름
    
        like_users.remove(user_id)
        self.update(post_id, {
            'like_users': like_users,
            'likes': len(like_users)
        })
        return True

    ## 조회 수 증가
    def increment_view_count(self, post_id: int) -> bool:
        post = self.find_by_id(post_id)
        if not post:
            return False
    
        current_views = post.get('view_count', 0)
        self.update(post_id, {'view_count': current_views + 1})
        return True

post_model = PostModel()