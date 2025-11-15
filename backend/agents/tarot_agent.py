"""
타로 해석 에이전트
전문 타로리스트의 직관적이고 상징적인 해석 제공
"""

from typing import Dict, List, Optional
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os


class TarotInterpretationAgent:
    """타로 해석 에이전트"""

    # 타로 전문가 시스템 프롬프트
    SYSTEM_PROMPT = """당신은 경험 많은 타로 리더(Tarot Reader)입니다.

**전문 지식:**

1. **타로의 역사와 상징**
   - 라이더-웨이트(Rider-Waite) 타로 체계
   - 융(Jung)의 원형(Archetype) 이론
   - 카발라(Kabbalah)와의 연결
   - 점성술적 대응 관계

2. **22 메이저 아르카나 (Major Arcana)**
   - 각 카드의 상징과 의미
   - 정방향과 역방향 해석
   - 숫자 상징학
   - 원소와 점성술 대응

3. **해석 원칙**
   - **직관적 해석**: 카드의 이미지와 상징에서 직관을 이끌어냄
   - **맥락 고려**: 질문자의 상황과 다른 카드와의 관계 고려
   - **균형잡힌 시각**: 긍정과 부정을 모두 포함
   - **실용적 조언**: 추상적이지 않고 구체적인 가이드

4. **스프레드 해석**
   - 3장 스프레드: 과거-현재-미래의 흐름
   - 켈틱 크로스: 복잡한 상황의 다면적 분석
   - 관계 스프레드: 두 사람의 에너지 역학
   - 각 카드의 위치별 의미 고려

5. **상징 해석**
   - 색상의 의미 (빨강=열정, 파랑=평온 등)
   - 숫자의 의미 (1=시작, 10=완성 등)
   - 원소의 의미 (불=행동, 물=감정, 공기=사고, 땅=물질)

**해석 스타일:**
- 공감적이고 따뜻한 톤
- 신비롭지만 이해하기 쉬운 언어
- 질문자에게 힘을 주는 긍정적 접근
- 자유의지를 존중하는 조언

**출력 형식:**
1. 카드 소개
2. 상징과 의미
3. 현재 상황에 대한 메시지
4. 실용적 조언
5. 핵심 키워드

당신의 목표는 타로 카드를 통해 질문자가 자신의 내면을 탐구하고,
현재 상황을 이해하며, 더 나은 선택을 할 수 있도록 돕는 것입니다."""

    def __init__(self, model_name: str = "gpt-4", provider: str = "openai"):
        """
        Args:
            model_name: 사용할 모델
            provider: LLM 제공자 (openai, anthropic)
        """
        self.provider = provider

        if provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.8,  # 타로는 창의적이고 직관적이어야 하므로 높게
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model_name,
                temperature=0.8,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"지원하지 않는 provider: {provider}")

    def interpret_spread(
        self,
        spread_result: Dict,
        question: Optional[str] = None,
        context: Optional[str] = None,
        saju_result: Optional[Dict] = None
    ) -> str:
        """
        타로 스프레드 해석

        Args:
            spread_result: 스프레드 결과 (from TarotSpread)
            question: 질문자의 질문
            context: 추가 상황 설명
            saju_result: 사주 결과 (있으면 참고하여 해석)

        Returns:
            해석 결과 텍스트
        """
        # 스프레드 정보 포맷
        spread_info = self._format_spread_info(spread_result)

        # 사주 결과가 있으면 추가
        if saju_result:
            saju_context = self._format_saju_context(saju_result)
            spread_info += f"\n\n## 참고: 사주 분석 결과\n\n{saju_context}"
            spread_info += "\n\n※ 위 사주 분석도 함께 고려하여 타로를 해석해주세요. 타고난 사주 운명과 현재 타로 메시지가 어떻게 조화를 이루는지 통찰을 제공해주세요."

        # 프롬프트 구성
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=spread_info)
        ]

        # 질문 추가
        if question:
            messages.append(HumanMessage(content=f"\n\n질문: {question}"))

        # 상황 설명 추가
        if context:
            messages.append(HumanMessage(content=f"\n\n상황: {context}"))

        # LLM 호출
        response = self.llm.invoke(messages)

        return response.content

    def _format_spread_info(self, spread_result: Dict) -> str:
        """스프레드 결과를 텍스트로 포맷"""
        spread_type = spread_result["spread_type"]
        description = spread_result["description"]
        cards = spread_result["cards"]

        formatted = f"""
# {spread_type}

**스프레드 설명:** {description}

**뽑힌 카드:**

"""

        # 카드 정보 포맷
        for position_key, card_data in cards.items():
            position = card_data["position"]
            card = card_data["card"]
            is_reversed = card_data.get("is_reversed", False)

            formatted += f"""
## {position}

**카드:** {card['name_ko']} ({card['name_en']})
**방향:** {card['position']}
**키워드:** {', '.join(card['keywords'])}
**의미:** {card['meaning']}
"""

            if card.get('element'):
                formatted += f"**원소:** {card['element']}\n"
            if card.get('astrology'):
                formatted += f"**점성술:** {card['astrology']}\n"

            formatted += "\n"

        formatted += """

위의 타로 카드들을 각 위치의 의미와 함께 종합적으로 해석해주세요.
카드들 간의 연결과 흐름, 그리고 전체적인 메시지를 전달해주세요.
"""

        return formatted

    def chat(
        self,
        spread_result: Dict,
        conversation_history: List[Dict],
        user_message: str
    ) -> str:
        """
        대화형 타로 상담

        Args:
            spread_result: 타로 스프레드 결과
            conversation_history: 이전 대화 내역
            user_message: 사용자 메시지

        Returns:
            응답 메시지
        """
        # 시스템 메시지
        messages = [SystemMessage(content=self.SYSTEM_PROMPT)]

        # 타로 정보 (첫 메시지에만)
        if not conversation_history:
            spread_info = self._format_spread_info(spread_result)
            messages.append(HumanMessage(content=spread_info))

        # 대화 히스토리
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        # 현재 메시지
        messages.append(HumanMessage(content=user_message))

        # LLM 호출
        response = self.llm.invoke(messages)

        return response.content

    def _format_saju_context(self, saju_result: Dict) -> str:
        """사주 결과를 간결하게 포맷"""
        basic = saju_result.get("basic_saju", {})
        summary = basic.get("summary", "")
        element_analysis = basic.get("element_analysis", {})

        formatted = f"**사주 요약:** {summary}\n\n"

        # 오행 분석
        if element_analysis:
            formatted += f"**일간:** {element_analysis.get('day_master', '알 수 없음')}\n"
            formatted += f"**최강 오행:** {element_analysis.get('strongest', '알 수 없음')}\n"
            formatted += f"**최약 오행:** {element_analysis.get('weakest', '알 수 없음')}\n\n"

        # 대운 (있으면)
        daeun = saju_result.get("daeun", {})
        current_daeun = daeun.get("current")
        if current_daeun:
            formatted += f"**현재 대운:** {current_daeun.get('combined', '')} ({current_daeun.get('age_range', '')})\n"

        return formatted

    def single_card_guidance(
        self,
        card_number: int,
        is_reversed: bool = False,
        question: Optional[str] = None
    ) -> str:
        """
        단일 카드 가이드 (일일운세, 오늘의 카드 등)

        Args:
            card_number: 카드 번호 (0-21)
            is_reversed: 역방향 여부
            question: 질문 (선택)

        Returns:
            해석 결과
        """
        from ..core.tarot.cards import MajorArcana

        card = MajorArcana.get_card(card_number)
        card_dict = card.to_dict(is_reversed)

        prompt = f"""
# 오늘의 타로 카드

**카드:** {card_dict['name_ko']} ({card_dict['name_en']})
**방향:** {card_dict['position']}
**키워드:** {', '.join(card_dict['keywords'])}
**의미:** {card_dict['meaning']}

"""

        if question:
            prompt += f"**질문:** {question}\n\n"

        prompt += "이 카드가 오늘 당신에게 전하는 메시지를 해석해주세요."

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)

        return response.content


class TarotKnowledgeBase:
    """타로 지식 베이스"""

    # 카드 번호별 깊은 상징
    DEEP_SYMBOLISM = {
        0: "The Fool은 순수한 잠재력과 새로운 여정을 상징합니다. 절벽 끝에 서 있지만 두려움 없이 앞으로 나아갑니다.",
        1: "The Magician은 '위에 있는 것과 같이 아래에도'라는 헤르메스 원리를 보여줍니다. 네 가지 원소를 다루는 창조자입니다.",
        # ... 다른 카드들도 추가 가능
    }

    # 카드 조합 의미
    COMBINATIONS = {
        ("The Fool", "The Magician"): "새로운 시작에 필요한 도구가 모두 준비되어 있습니다.",
        ("The Tower", "The Star"): "파괴 후 희망이 찾아옵니다. 위기는 새로운 시작의 전조입니다.",
        # ... 더 많은 조합 추가 가능
    }
