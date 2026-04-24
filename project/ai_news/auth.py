import os
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from supabase import create_client, Client
import jwt

router = APIRouter()

# Supabase 클라이언트 초기화
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: SUPABASE_URL or SUPABASE_KEY is missing")

# 일반 인증용 클라이언트 (anon key)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# 관리자용 클라이언트 (service_role key) - 회원 탈퇴 등 admin 작업에 사용
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else None

class UserAuth(BaseModel):
    email: EmailStr 
    password: str
    username: Optional[str] = None


def get_user_id_from_token(authorization: str) -> str:
    """Bearer 토큰에서 user_id를 추출"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다. 다시 로그인해주세요.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"유효하지 않은 토큰입니다: {str(e)}")


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


@router.delete("/delete-account")
async def delete_account(authorization: str = Header(None)):
    """회원 탈퇴 - 유저 삭제 시 CASCADE로 todos, memos, calendars 데이터 자동 삭제"""
    if not supabase_admin:
        raise HTTPException(status_code=500, detail="관리자 설정이 안 되어있습니다. SUPABASE_SERVICE_ROLE_KEY를 확인해주세요.")
    
    user_id = get_user_id_from_token(authorization)
    
    try:
        # Supabase Admin API로 유저 삭제 (CASCADE로 관련 데이터 자동 삭제)
        supabase_admin.auth.admin.delete_user(user_id)
        return {"message": "회원 탈퇴가 완료되었습니다. 그동안 이용해 주셔서 감사합니다."}
    except Exception as e:
        print(f"[Delete Account Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"회원 탈퇴 중 오류가 발생했습니다: {str(e)}")

