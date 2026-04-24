import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from supabase import create_client, Client

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: SUPABASE_URL or SUPABASE_KEY is missing")

# FastAPI가 로드될 때만 Client 생성 (None 검사)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

class UserAuth(BaseModel):
    email: EmailStr 
    password: str
    username: Optional[str] = None

@router.post("/signup")
async def signup(user: UserAuth):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    try:
        # Supabase Auth 회원가입 (username은 메타데이터로 저장)
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "username": user.username
                }
            }
        })
        
        # 이메일 중복 시 Supabase는 성공처럼 응답하지만 user의 id가 없거나 identities가 비어있을 수 있음
        if response.user and not response.user.identities:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
            
        return {"message": "회원가입 성공! (이메일 인증이 필요한 경우 이메일을 확인해주세요.)", "user_id": response.user.id}
    except Exception as e:
        # 이미 존재하는 이메일이거나 비밀번호 규칙 미달 등 오류
        if isinstance(e, HTTPException):
            raise e
        print(f"[Signup Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserAuth):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    try:
        # Supabase를 통한 로그인 처리
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        return {
            "message": "로그인 성공", 
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "username": response.user.user_metadata.get("username")
            }
        }
    except Exception as e:
        print(f"[Login Error] {type(e).__name__}: {e}")
        error_msg = str(e).lower()
        if "email not confirmed" in error_msg:
            raise HTTPException(status_code=401, detail="이메일 인증이 완료되지 않았습니다. 가입 시 입력한 이메일의 인증 링크를 클릭해주세요.")
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
