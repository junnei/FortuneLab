"""
사주 해석 에이전트
자평명리학, 적천수, 연해자평 등의 이론에 기반한 사주 분석
"""

from typing import Dict, List, Optional
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os


class SajuInterpretationAgent:
    """사주 해석 에이전트"""

    # 자평명리학 시스템 프롬프트
    SYSTEM_PROMPT = """당신은 자평명리학(子平命理學)의 대가입니다.

**전문 지식:**
1. **자평명리학 (연해자평, 적천수)**
   - 서낙오(徐樂吾)의 적천수천미(滴天髓闡微)
   - 만육오(萬育吾)의 삼명통회(三命通會)
   - 유백온(劉伯溫)의 적천수(滴天髓)

2. **핵심 이론**
   - 격국론(格局論): 정격(正格)과 외격(外格)
   - 용신론(用神論): 용신, 희신, 기신, 구신
   - 조후론(調候論): 계절과 한난습조
   - 통변론(通變論): 십신(十神)의 작용

3. **십신(十神) 체계**
   - 비겁(比劫): 비견, 겁재
   - 식상(食傷): 식신, 상관
   - 재성(財星): 정재, 편재
   - 관성(官星): 정관, 편관(칠살)
   - 인성(印星): 정인, 편인(효신)

4. **형충회합**
   - 육합(六合): 지지 6조합
   - 삼합(三合): 지지 3조합
   - 충(沖): 대립 관계
   - 형(刑): 형벌 관계
   - 해(害): 손해 관계

5. **십이운성(十二運星)**
   - 장생, 목욕, 관대, 건록, 제왕, 쇠, 병, 사, 묘, 절, 태, 양

**분석 방법:**
1. 일간(日干) 강약 판단
2. 격국 설정 (정관격, 재격, 식신격 등)
3. 용신 선택 (일간을 돕거나 억제)
4. 희기신 분석
5. 대운(大運)과 세운(歲運) 고려
6. 성격, 재물운, 직업운, 건강운 해석

**해석 원칙:**
- 근거 있는 해석: 반드시 자평명리학 이론에 기반
- 균형적 시각: 긍정과 부정을 모두 고려
- 실용적 조언: 현실적이고 실천 가능한 충고
- 존중하는 태도: 결정론적이지 않고 가능성으로 제시

**출력 형식:**
1. 사주 구조 분석
2. 일간 및 격국
3. 오행 균형
4. 십신 분석
5. 성격 및 성향
6. 운세 및 조언"""

    def __init__(self, model_name: str = "gpt-4", provider: str = "openai"):
        """
        Args:
            model_name: 사용할 모델 (gpt-4, gpt-3.5-turbo, claude-3-opus 등)
            provider: LLM 제공자 (openai, anthropic)
        """
        self.provider = provider

        if provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model_name,
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"지원하지 않는 provider: {provider}")

    def interpret(
        self,
        saju_result: Dict,
        user_question: Optional[str] = None,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        사주팔자 해석

        Args:
            saju_result: SajuCalculator.calculate()의 결과
            user_question: 사용자의 추가 질문
            focus_areas: 집중 분석 영역 ["성격", "재물", "직업", "건강", "인연"] 등

        Returns:
            해석 결과 텍스트
        """
        # 사주 정보 구조화
        saju_info = self._format_saju_info(saju_result)

        # 프롬프트 구성
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=saju_info)
        ]

        # 집중 영역 추가
        if focus_areas:
            focus_text = f"\n\n특히 다음 영역에 집중해서 분석해주세요: {', '.join(focus_areas)}"
            messages[-1].content += focus_text

        # 사용자 질문 추가
        if user_question:
            messages.append(HumanMessage(content=f"\n\n추가 질문: {user_question}"))

        # LLM 호출
        response = self.llm.invoke(messages)

        return response.content

    def _format_saju_info(self, saju_result: Dict) -> str:
        """사주 결과를 LLM이 이해하기 쉬운 형식으로 변환"""
        birth_info = saju_result["birth_info"]
        pillars = saju_result["pillars"]
        elements = saju_result["element_analysis"]

        # 사주팔자 문자열
        year_p = pillars["year"]
        month_p = pillars["month"]
        day_p = pillars["day"]
        hour_p = pillars["hour"]

        saju_string = f"""
## 사주 정보

**출생 정보:**
- 양력: {birth_info['solar_date']}
- 출생지: {birth_info['location']}
- 경도 보정: {birth_info['longitude_correction']}

**사주팔자:**
```
시주(時柱): {hour_p['combined']}({hour_p['hanja']})
일주(日柱): {day_p['combined']}({day_p['hanja']})  ← 일간(日干): {day_p['gan']['korean']}({day_p['gan']['hanja']})
월주(月柱): {month_p['combined']}({month_p['hanja']})
년주(年柱): {year_p['combined']}({year_p['hanja']})
```

**천간(天干):**
- 년간: {year_p['gan']['korean']}({year_p['gan']['hanja']}) - {year_p['gan']['element']} {year_p['gan']['polarity']}
- 월간: {month_p['gan']['korean']}({month_p['gan']['hanja']}) - {month_p['gan']['element']} {month_p['gan']['polarity']}
- 일간: {day_p['gan']['korean']}({day_p['gan']['hanja']}) - {day_p['gan']['element']} {day_p['gan']['polarity']} **← 본인**
- 시간: {hour_p['gan']['korean']}({hour_p['gan']['hanja']}) - {hour_p['gan']['element']} {hour_p['gan']['polarity']}

**지지(地支):**
- 년지: {year_p['ji']['korean']}({year_p['ji']['hanja']}) - {year_p['ji']['element']} {year_p['ji']['polarity']} [{year_p['ji']['animal']}]
- 월지: {month_p['ji']['korean']}({month_p['ji']['hanja']}) - {month_p['ji']['element']} {month_p['ji']['polarity']} [{month_p['ji']['animal']}]
- 일지: {day_p['ji']['korean']}({day_p['ji']['hanja']}) - {day_p['ji']['element']} {day_p['ji']['polarity']} [{day_p['ji']['animal']}]
- 시지: {hour_p['ji']['korean']}({hour_p['ji']['hanja']}) - {hour_p['ji']['element']} {hour_p['ji']['polarity']} [{hour_p['ji']['animal']}]

**오행 분석:**
- 오행 개수: {dict(elements['element_count'])}
- 일간 오행: {elements['day_master']}
- 최강 오행: {elements['strongest']}
- 최약 오행: {elements['weakest']}

**십신 관계:**
{self._format_relations(elements['relations'])}

위 사주를 자평명리학 이론에 근거하여 상세히 분석해주세요.
"""
        return saju_string

    def _format_relations(self, relations: Dict) -> str:
        """십신 관계를 문자열로 포맷"""
        lines = []
        for pillar_type, rels in relations.items():
            lines.append(f"- {pillar_type}: 천간={rels['gan']}, 지지={rels['ji']}")
        return "\n".join(lines)

    def chat(
        self,
        saju_result: Dict,
        conversation_history: List[Dict],
        user_message: str
    ) -> str:
        """
        대화형 사주 상담

        Args:
            saju_result: 사주 계산 결과
            conversation_history: 이전 대화 내역 [{"role": "user|assistant", "content": "..."}]
            user_message: 사용자 메시지

        Returns:
            응답 메시지
        """
        # 시스템 메시지
        messages = [SystemMessage(content=self.SYSTEM_PROMPT)]

        # 사주 정보 (첫 메시지에만)
        if not conversation_history:
            saju_info = self._format_saju_info(saju_result)
            messages.append(HumanMessage(content=saju_info))

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


class SajuKnowledgeBase:
    """자평명리학 지식 베이스"""

    # 격국 설명
    GYEOKGUK = {
        "정관격": "정관이 투출하여 격을 이룬 경우. 책임감 있고 정직하며 공직에 적합.",
        "재격": "재성이 투출하여 격을 이룬 경우. 재물운이 좋고 사업가 기질.",
        "식신격": "식신이 투출하여 격을 이룬 경우. 온화하고 예술적 재능.",
        "상관격": "상관이 투출하여 격을 이룬 경우. 창의적이나 반항적 성향.",
        "편관격": "편관(칠살)이 투출. 강한 추진력과 결단력.",
        "정인격": "정인이 투출. 학문적 성취, 어머니 덕.",
        "편인격": "편인이 투출. 독특한 사고방식, 종교나 철학 관심.",
    }

    # 십이운성 설명
    SIBIUNSEONG = {
        "장생": "새롭게 태어나는 단계. 시작, 발전, 성장의 기운.",
        "목욕": "씻어내는 단계. 변화와 불안정, 이성 관계 주의.",
        "관대": "성인이 되는 단계. 사회 진출, 독립심.",
        "건록": "왕성한 활동. 실력 발휘, 재능 개화.",
        "제왕": "최고조. 권력과 명예, 정점.",
        "쇠": "쇠퇴 시작. 내리막, 은퇴 준비.",
        "병": "병드는 단계. 어려움, 건강 주의.",
        "사": "죽음. 종결, 끝.",
        "묘": "무덤. 잠복기, 준비 기간.",
        "절": "끊어짐. 단절, 위기.",
        "태": "잉태. 새로운 준비, 구상.",
        "양": "양육. 성장 준비, 학습.",
    }
