"""
FastAPI 메인 애플리케이션
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .api.routes import router

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="FortuneLab API",
    description="사주/타로 AI 에이전트 웹서비스 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js 개발 서버
        "https://*.vercel.app",    # Vercel 배포
        os.getenv("FRONTEND_URL", "")  # 환경 변수로 설정된 프론트엔드 URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(router, prefix="/api")


# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    print("🚀 FortuneLab API 시작!")
    print(f"📍 OpenAI API Key: {'✓ 설정됨' if os.getenv('OPENAI_API_KEY') else '✗ 미설정'}")
    print(f"📍 Anthropic API Key: {'✓ 설정됨' if os.getenv('ANTHROPIC_API_KEY') else '✗ 미설정'}")


# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    print("👋 FortuneLab API 종료")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 개발 모드
    )
