import json
from pathlib import Path
from typing import List, Optional
import hashlib

class UserModel:
    def __init__(self):
        self.db_path = Path("data/users.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    ## 모든 사용자정보 읽기
    def _read_all(self) -> List[dict]:
        if not self.db_path.exists():
            return[]
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    ## 모든 사용자정보 쓰기
    def _write_all(self, users: List[dict]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    ## 다음 ID 찾기
    def get_next_id(self) -> int:
        users = self._read_all()
        if not users:
            return 1
        return max(user["id"] for user in users) + 1
    
    ## ID로 사용자 찾기
    def find_by_id(self, user_id: int) -> Optional[dict]:
        users = self._read_all()
        return next((user for user in users if user['id'] == user_id), None)
    
    ## 다음 ID 생성
    def get_next_id(self) -> int:
        users = self._read_all()
        if not users:
            return 1
        
    ## 이메일로 사용자 찾기
    def find_by_email(self, email: str) -> Optional[dict]:
        users = self._read_all()
        return next((user for user in users if user['email'] == email), None)
    
    ## 닉네임으로 사용자 찾기
    def find_by_nickname(self, nickname: str) -> Optional[dict]:
        users = self._read_all()
        return next((user for user in users if user['nickname'] == nickname), None)
    
    ## 사용자 생성
    def create(self, user_data: dict) -> dict:
        users = self._read_all()
        user_data['id'] = self.get_next_id()
        users.append(user_data)
        self._write_all(users)
        return user_data
    
    ## 사용자 정보 업데이트
    def update(self, user_id: int, updates: dict) -> Optional[dict]:
        users = self._read_all()
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return None
        user.update(updates)
        self._write_all(users)
        return user
    
    ## 사용자 삭제
    def delete(self, user_id: int) -> bool:
        users = self._read_all()
        original_length = len(users)
        users = [u for u in users if u['id'] != user_id]
        if len(users) < original_length:
            self._write_all(users)
            return True
        return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """비밀번호 해싱"""
        return hashlib.sha256(password.encode()).hexdigest()

user_model = UserModel()    