"""
FastAPI 라우트 정의
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict

from ..models.schemas import (
    SajuRequest, SajuResponse,
    SajuInterpretRequest, SajuInterpretResponse,
    TarotDrawRequest, TarotDrawResponse,
    TarotInterpretRequest, TarotInterpretResponse,
    ChatRequest, ChatResponse,
    HealthResponse
)
from ..core.saju import calculate_manseryeok, Manseryeok
from ..core.tarot.spread import get_spread
from ..agents.saju_agent import SajuInterpretationAgent
from ..agents.tarot_agent import TarotInterpretationAgent

# 라우터 생성
router = APIRouter()

# 에이전트 인스턴스 (싱글톤)
saju_agent = None
tarot_agent = None


def get_saju_agent():
    """사주 에이전트 싱글톤"""
    global saju_agent
    if saju_agent is None:
        saju_agent = SajuInterpretationAgent(model_name="gpt-4", provider="openai")
    return saju_agent


def get_tarot_agent():
    """타로 에이전트 싱글톤"""
    global tarot_agent
    if tarot_agent is None:
        tarot_agent = TarotInterpretationAgent(model_name="gpt-4", provider="openai")
    return tarot_agent


# ===== 헬스 체크 =====

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """헬스 체크 엔드포인트"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


# ===== 사주 API =====

@router.post("/saju/calculate", response_model=SajuResponse)
async def calculate_saju(request: SajuRequest):
    """
    사주 만세력 계산 (결정론적)

    생년월일시, 성별, 출생지를 입력받아 만세력을 계산합니다.
    - 사주팔자
    - 대운/세운
    - 형충회합
    - 십이운성
    - 신살
    """
    try:
        # 날짜 파싱
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d %H:%M")

        # 만세력 계산
        result = calculate_manseryeok(
            birth_date=birth_date,
            gender=request.gender,
            birth_location=request.birth_location,
            is_lunar=request.is_lunar,
            current_age=request.current_age,
            target_year=request.target_year
        )

        return SajuResponse(
            success=True,
            data=result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/saju/interpret", response_model=SajuInterpretResponse)
async def interpret_saju(request: SajuInterpretRequest):
    """
    사주 해석 (AI 에이전트)

    만세력 계산 결과를 AI 에이전트가 자평명리학 기반으로 해석합니다.
    """
    try:
        agent = get_saju_agent()

        # 해석
        interpretation = agent.interpret(
            saju_result=request.manseryeok_result,
            user_question=request.question,
            focus_areas=request.focus_areas
        )

        return SajuInterpretResponse(
            success=True,
            interpretation=interpretation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 타로 API =====

@router.post("/tarot/draw", response_model=TarotDrawResponse)
async def draw_tarot(request: TarotDrawRequest):
    """
    타로 카드 뽑기

    선택한 스프레드 타입에 따라 타로 카드를 뽑습니다.
    - three_card: 3장 (과거/현재/미래)
    - celtic_cross: 10장 (켈틱 크로스)
    - relationship: 5장 (관계)
    - yes_no: 1장 (예/아니오)
    """
    try:
        # 스프레드 가져오기
        spread = get_spread(request.spread_type.value)

        # 카드 뽑기
        spread_result = spread.draw(allow_reversed=request.allow_reversed)

        # 질문 추가
        if request.question:
            spread_result["question"] = request.question

        return TarotDrawResponse(
            success=True,
            spread_result=spread_result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tarot/interpret", response_model=TarotInterpretResponse)
async def interpret_tarot(request: TarotInterpretRequest):
    """
    타로 해석 (AI 에이전트)

    뽑힌 타로 카드를 AI 에이전트가 전문적으로 해석합니다.
    """
    try:
        agent = get_tarot_agent()

        # 해석
        interpretation = agent.interpret_spread(
            spread_result=request.spread_result,
            question=request.question,
            context=request.context
        )

        return TarotInterpretResponse(
            success=True,
            interpretation=interpretation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 채팅 API =====

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    대화형 상담

    사주 또는 타로 결과를 바탕으로 AI 에이전트와 대화합니다.
    """
    try:
        # 서비스 타입에 따라 에이전트 선택
        if request.service_type == "saju":
            agent = get_saju_agent()
            history = [{"role": msg.role, "content": msg.content} for msg in request.conversation_history]
            reply = agent.chat(
                saju_result=request.session_data,
                conversation_history=history,
                user_message=request.user_message
            )
        elif request.service_type == "tarot":
            agent = get_tarot_agent()
            history = [{"role": msg.role, "content": msg.content} for msg in request.conversation_history]
            reply = agent.chat(
                spread_result=request.session_data,
                conversation_history=history,
                user_message=request.user_message
            )
        else:
            raise ValueError(f"Unknown service type: {request.service_type}")

        return ChatResponse(
            success=True,
            reply=reply
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 기타 =====

@router.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "FortuneLab API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "saju_calculate": "/saju/calculate",
            "saju_interpret": "/saju/interpret",
            "tarot_draw": "/tarot/draw",
            "tarot_interpret": "/tarot/interpret",
            "chat": "/chat"
        }
    }
