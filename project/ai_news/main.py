import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from auth import router as auth_router
from todos import router as todos_router

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.1-flash-lite')

app = FastAPI(title="AI News API")

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

# 항상 허용할 origin (로컬 개발 환경)
default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
for default_origin in default_origins:
    if default_origin not in allowed_origins:
        allowed_origins.append(default_origin)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(todos_router, prefix="/api", tags=["data"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsItem(BaseModel):
    title: str
    link: str

class NewsResponse(BaseModel): 
    summary: str
    news_list: List[NewsItem]

def fetch_rss_news(keyword: str):
    keyword = keyword.strip()
    if keyword:
        url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    items = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")
        
    news_list = []
    
    # 구글 뉴스에서 실패하거나 아이템을 못 가져오면 폴백(Fallback) 시도
    if not items:
        # 1. 키워드가 있을 경우 Daum 뉴스 검색 결과 스크래핑 시도
        if keyword:
            daum_url = f"https://search.daum.net/search?w=news&q={keyword}"
            daum_response = requests.get(daum_url, headers=headers)
            if daum_response.status_code == 200:
                daum_soup = BeautifulSoup(daum_response.content, "html.parser")
                daum_articles = daum_soup.select(".item-title .tit-g a")
                for a in daum_articles[:10]:
                    title = a.text.strip()
                    link = a.get("href", "")
                    if title and link:
                        news_list.append({"title": title, "link": link})
                
                if news_list:
                    return news_list # 성공적으로 가져왔다면 바로 반환
        
        # 2. 키워드가 없거나 Daum 검색에서도 실패한 경우 동아일보 전체 RSS로 최후 폴백
        fallback_url = "https://rss.donga.com/total.xml"
        fallback_response = requests.get(fallback_url, headers=headers)
        if fallback_response.status_code == 200:
            soup = BeautifulSoup(fallback_response.content, "xml")
            all_items = soup.find_all("item")
            
            # 키워드가 있다면 제목에서 키워드 필터링
            if keyword:
                items = [item for item in all_items if keyword.lower() in item.title.text.lower()]
            else:
                items = all_items

    # 일반적인 RSS 파싱 (구글 뉴스 성공 또는 동아일보 폴백 성공 시)
    if not news_list:
        # 최신 뉴스 10개만 가져오기
        for item in items[:10]:
            title = item.title.text.strip()
            link = item.link.text.strip()
            news_list.append({"title": title, "link": link})
        
    return news_list

@app.get("/api/news", response_model=NewsResponse)
async def get_news_summary(keyword: str = Query("", description="검색할 뉴스 키워드")):
    try:
        news_data = fetch_rss_news(keyword)
        
        if not news_data:
            raise HTTPException(status_code=404, detail="뉴스를 찾을 수 없습니다.")
            
        subject_message = f"'{keyword}' 관련 최신" if keyword.strip() else "최신 종합"
        news_titles = "\n".join([f"- {n['title']}" for n in news_data])
        
        prompt = f"""
        너는 트렌드에 민감하고 통찰력 있는 전문 에디터야.
        아래는 오늘 스크랩된 {subject_message} 뉴스 제목들이야.
        이 제목들을 꼼꼼하게 읽고, 오늘 사람들의 주요 관심사나 핵심 트렌드를 5가지의 불릿 포인트로 뽑아서 재밌고 알기 쉽게 요약해줘.
        딱딱하지 않은 친근한 말투로 해주고 적절한 이모지를 필요하면 섞어줘!
        
        [오늘의 수집된 기사 제목들]
        {news_titles}
        """
        
        response = model.generate_content(prompt)
        
        return NewsResponse(
            summary=response.text,
            news_list=news_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
