import json
from pathlib import Path
from typing import List, Optional

class CommentModel:
    def __init__(self):
        self.db_path = Path("data/comments.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    ## 모든 댓글 읽기
    def _read_all(self) -> List[dict]:
        if not self.db_path.exists():
            return []
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    ## 모든 댓글 쓰기
    def _write_all(self, comments: List[dict]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
    
    ## 다음 id 생성
    def get_next_id(self) -> int:
        comments = self._read_all()
        if not comments:
            return 1
        return max(comment["id"] for comment in comments) + 1
    
    ## id로 댓글 찾기
    def find_by_id(self, comment_id: int) -> Optional[dict]:
        comments = self._read_all()
        return next((c for c in comments if c['id'] == comment_id), None)
    
    ## id로 게시글의 댓글 조회
    def find_by_post_id(self, post_id: int) -> List[dict]:
        comments = self._read_all()
        post_comments = [c for c in comments if c['post_id'] == post_id]
        # 최신순 정렬
        return sorted(post_comments, key=lambda x: x['created_at'], reverse=True)
    
    ## 댓글 생성
    def create(self, comment_data: dict) -> dict:
        comments = self._read_all()
        comment_data['id'] = self.get_next_id()
        comments.append(comment_data)
        self._write_all(comments)
        return comment_data
    
    ## 댓글 수정
    def update(self, comment_id: int, updates: dict) -> Optional[dict]:
        comments = self._read_all()
        comment = next((c for c in comments if c['id'] == comment_id), None)
        if not comment:
            return None
        comment.update(updates)
        self._write_all(comments)
        return comment
    
    ## 댓글 삭제
    def delete(self, comment_id: int) -> bool:
        comments = self._read_all()
        original_length = len(comments)
        comments = [c for c in comments if c['id'] != comment_id]
        if len(comments) < original_length:
            self._write_all(comments)
            return True
        return False
    
    ## 댓글 수
    def count_by_post_id(self, post_id: int) -> int:
        comments = self._read_all()
        return len([c for c in comments if c['post_id'] == post_id])

comment_model = CommentModel()