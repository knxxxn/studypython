import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, List, Optional
from supabase import create_client, Client
import jwt

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")

# service_role key로 클라이언트 생성 (RLS 우회 - 서버에서 user_id로 직접 필터링)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else None

if not supabase:
    print("Warning: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing - 투두/메모 API 비활성")


def get_user_id_from_token(authorization: str) -> str:
    """Bearer 토큰에서 user_id를 추출"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
    
    token = authorization.replace("Bearer ", "")
    try:
        # Supabase JWT는 HS256으로 서명됨
        # JWT_SECRET이 없으면 verify 없이 디코딩 (개발용)
        if JWT_SECRET:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        else:
            payload = jwt.decode(token, options={"verify_signature": False})
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다. 다시 로그인해주세요.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"유효하지 않은 토큰입니다: {str(e)}")


# ── 투두 ──

class TodoItem(BaseModel):
    text: str
    done: bool = False

class TodosSaveRequest(BaseModel):
    """프론트엔드에서 날짜별 투두를 통째로 보내는 구조
    예: { "2026-04-24": [{"text":"할 일","done":false}], ... }
    """
    data: Dict[str, List[TodoItem]]

@router.post("/todos")
async def save_todos(body: dict, authorization: str = Header(None)):
    """투두 전체를 날짜별로 저장 (Upsert 방식)"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    
    user_id = get_user_id_from_token(authorization)
    
    try:
        # 기존 데이터 전부 삭제 후 새로 삽입 (전체 동기화 방식)
        supabase.table("todos").delete().eq("user_id", user_id).execute()
        
        rows = []
        for date_str, items in body.items():
            if isinstance(items, list) and len(items) > 0:
                rows.append({
                    "user_id": user_id,
                    "date": date_str,
                    "items": items  # JSON 배열 그대로 저장
                })
        
        if rows:
            supabase.table("todos").insert(rows).execute()
        
        return {"message": "투두 저장 완료", "count": len(rows)}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"[Todos Save Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/todos")
async def get_todos(authorization: str = Header(None)):
    """로그인한 유저의 전체 투두를 가져옴"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    
    user_id = get_user_id_from_token(authorization)
    
    try:
        response = supabase.table("todos").select("date, items").eq("user_id", user_id).execute()
        
        # { "2026-04-24": [...], "2026-04-25": [...] } 형태로 변환
        result = {}
        for row in response.data:
            result[row["date"]] = row["items"]
        
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"[Todos Get Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── 메모 ──

@router.post("/memos")
async def save_memos(body: dict, authorization: str = Header(None)):
    """메모 전체를 날짜별로 저장 (Upsert 방식)"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    
    user_id = get_user_id_from_token(authorization)
    
    try:
        supabase.table("memos").delete().eq("user_id", user_id).execute()
        
        rows = []
        for date_str, content in body.items():
            if content and isinstance(content, str) and content.strip():
                rows.append({
                    "user_id": user_id,
                    "date": date_str,
                    "content": content
                })
        
        if rows:
            supabase.table("memos").insert(rows).execute()
        
        return {"message": "메모 저장 완료", "count": len(rows)}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"[Memos Save Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memos")
async def get_memos(authorization: str = Header(None)):
    """로그인한 유저의 전체 메모를 가져옴"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase 설정이 안 되어있습니다.")
    
    user_id = get_user_id_from_token(authorization)
    
    try:
        response = supabase.table("memos").select("date, content").eq("user_id", user_id).execute()
        
        # { "2026-04-24": "메모 내용", ... } 형태로 변환
        result = {}
        for row in response.data:
            result[row["date"]] = row["content"]
        
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(f"[Memos Get Error] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
