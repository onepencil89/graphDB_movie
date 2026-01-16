from fastapi import FastAPI, Request, Query
from movie import main_chain
# FastAPI() 객체 생성

from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML 템플릿 경로 등록
templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def home(request: Request, query: str = Query(..., description="영화 관련 질문을 입력하세요")):
    # 1. 로직 실행
    response = main_chain(query)
    
    # 2. 터미널 확인용
    print(f"질문: {query}")
    print(f"답변: {response}")
    
    # 3. 결과 반환 (Request 객체는 제외하고 데이터만 반환하거나, 템플릿에 넣어야 함)
    return {
        "user_query": query,
        "answer": response
    }