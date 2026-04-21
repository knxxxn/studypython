import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(page_title="나만의 AI 뉴스 요약봇", page_icon="📰", layout="centered")

st.title("📰 AI 뉴스 요약 페이지")
st.write("오늘의 주요 IT 뉴스를 모아 AI가 요약해 드립니다.")

# 1. .env 파일에서 환경 변수(API 키) 불러오기
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. 키워드 입력 화면
st.markdown("---")
search_keyword = st.text_input("🔍 관심 있는 뉴스 키워드를 자유롭게 입력해 보세요:", value="IT 스타트업")

# 3. 뉴스 크롤링 함수 (선택한 키워드 활용)
@st.cache_data(ttl=3600) # 1시간 동안 데이터를 캐싱
def fetch_news(keyword):
    # 구글 한국 뉴스 검색 결과 RSS (키워드를 동적으로 넣음)
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
        
    soup = BeautifulSoup(response.content, "xml") # RSS 데이터 파싱
    items = soup.find_all("item")
    
    news_list = []
    # 최신 뉴스 10개만 가져오기
    for item in items[:10]:
        title = item.title.text
        link = item.link.text
        news_list.append({"title": title, "link": link})
        
    return news_list

# 4. 메인 화면 - 실행 버튼
if st.button(f"🚀 '{search_keyword}' 트렌드 스크랩 & 요약하기", type="primary"):
    with st.spinner(f"'{search_keyword}' 관련 뉴스를 AI가 분석하는 중입니다... 잠시만 기다려주세요 ⏳"):
        try:
            # 데이터 수집 실행 (입력받은 키워드 던져주기)
            news_data = fetch_news(search_keyword)
            
            # 수집된 원본 뉴스 목록 보여주기 (접었다 펴기)
            with st.expander("방금 수집된 원본 뉴스 10개 보기"):
                for i, news in enumerate(news_data):
                    st.markdown(f"{i+1}. [{news['title']}]({news['link']})")
            
            # AI에 전달할 프롬프트(명령어) 준비
            # 제목들을 하나로 합칩니다.
            news_titles = "\n".join([f"- {n['title']}" for n in news_data])
            
            prompt = f"""
            너는 트렌드에 민감하고 통찰력 있는 전문 에디터야.
            아래는 오늘 스크랩된 '{search_keyword}' 관련 최신 뉴스 제목들이야.
            이 제목들을 꼼꼼하게 읽고, 오늘 사람들의 주요 관심사나 핵심 트렌드를 3가지의 불릿 포인트로 뽑아서 재밌고 알기 쉽게 요약해줘.
            딱딱하지 않은 친근한 말투로 해주고 적절한 이모지를 필요하면 섞어줘!
            
            [오늘의 수집된 기사 제목들]
            {news_titles}
            """
            
            # Gemini AI 호출
            genai.configure(api_key=api_key)
            # 최신 버전인 gemini-2.5-flash 모델 사용
            model = genai.GenerativeModel('gemini-2.5-flash') 
            response = model.generate_content(prompt)
            
            # 결과 출력
            st.success("분석이 완료되었습니다!")
            
            st.markdown("### ✨ AI가 읽어주는 오늘의 트렌드 인사이트")
            st.info(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
