"""
Pydantic 스키마 정의
API 요청/응답 모델
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


# ===== 공통 =====

class ServiceType(str, Enum):
    """서비스 타입"""
    SAJU = "saju"
    TAROT = "tarot"


# ===== 사주 관련 =====

class SajuRequest(BaseModel):
    """사주 계산 요청"""
    birth_date: str = Field(..., description="생년월일시 (YYYY-MM-DD HH:MM 형식)", example="1990-05-15 14:30")
    gender: str = Field(..., description="성별 (남/여)", example="남")
    birth_location: Optional[str] = Field(None, description="출생지", example="서울")
    is_lunar: bool = Field(False, description="음력 여부")
    is_leap_month: bool = Field(False, description="윤달 여부 (음력인 경우)")
    current_age: Optional[int] = Field(None, description="현재 나이 (대운 확인용)", example=35)
    target_year: Optional[int] = Field(None, description="분석 대상 년도 (세운 계산용)", example=2025)


class SajuResponse(BaseModel):
    """사주 계산 응답"""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None


class SajuInterpretRequest(BaseModel):
    """사주 해석 요청"""
    manseryeok_result: Dict = Field(..., description="만세력 계산 결과")
    question: Optional[str] = Field(None, description="추가 질문")
    focus_areas: Optional[List[str]] = Field(None, description="집중 분석 영역")


class SajuInterpretResponse(BaseModel):
    """사주 해석 응답"""
    success: bool
    interpretation: Optional[str] = None
    error: Optional[str] = None


# ===== 타로 관련 =====

class TarotSpreadType(str, Enum):
    """타로 스프레드 타입"""
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    RELATIONSHIP = "relationship"
    YES_NO = "yes_no"


class TarotDrawRequest(BaseModel):
    """타로 카드 뽑기 요청"""
    spread_type: TarotSpreadType = Field(..., description="스프레드 타입")
    allow_reversed: bool = Field(True, description="역방향 허용 여부")
    question: Optional[str] = Field(None, description="질문")


class TarotDrawResponse(BaseModel):
    """타로 카드 뽑기 응답"""
    success: bool
    spread_result: Optional[Dict] = None
    error: Optional[str] = None


class TarotInterpretRequest(BaseModel):
    """타로 해석 요청"""
    spread_result: Dict = Field(..., description="타로 스프레드 결과")
    question: Optional[str] = Field(None, description="질문")
    context: Optional[str] = Field(None, description="상황 설명")


class TarotInterpretResponse(BaseModel):
    """타로 해석 응답"""
    success: bool
    interpretation: Optional[str] = None
    error: Optional[str] = None


# ===== 채팅 관련 =====

class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: str = Field(..., description="역할 (user/assistant)")
    content: str = Field(..., description="메시지 내용")


class ChatRequest(BaseModel):
    """채팅 요청"""
    service_type: ServiceType = Field(..., description="서비스 타입")
    session_data: Dict = Field(..., description="세션 데이터 (사주 결과 또는 타로 결과)")
    conversation_history: List[ChatMessage] = Field([], description="대화 히스토리")
    user_message: str = Field(..., description="사용자 메시지")


class ChatResponse(BaseModel):
    """채팅 응답"""
    success: bool
    reply: Optional[str] = None
    error: Optional[str] = None


# ===== 헬스 체크 =====

class HealthResponse(BaseModel):
    """헬스 체크 응답"""
    status: str
    timestamp: str
    version: str
