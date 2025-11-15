"""
만세력 종합 계산 시스템

사주팔자 + 대운 + 세운 + 형충회합 + 십이운성 + 신살
모든 계산을 통합하여 제공하는 결정론적(deterministic) 시스템
"""

from datetime import datetime
from typing import Dict, Optional
from .calculator import SajuCalculator
from .daeun import DaeunCalculator, SeunCalculator
from .hyeongchung import HyeongchungAnalyzer
from .sibiunseong import SibiUnseong
from .sinsal import Sinsal


class Manseryeok:
    """만세력 종합 계산 시스템"""

    def __init__(self):
        self.saju_calculator = SajuCalculator()

    def calculate_full(
        self,
        birth_date: datetime,
        gender: str,  # "남" 또는 "여"
        birth_location: Optional[str] = None,
        is_lunar: bool = False,
        is_leap_month: bool = False,
        current_age: Optional[int] = None,
        target_year: Optional[int] = None
    ) -> Dict:
        """
        만세력 전체 계산 (결정론적 계산만)

        Args:
            birth_date: 생년월일시
            gender: 성별 ("남" 또는 "여")
            birth_location: 출생지
            is_lunar: 음력 여부
            is_leap_month: 윤달 여부
            current_age: 현재 나이 (대운 확인용)
            target_year: 분석 대상 년도 (세운 계산용)

        Returns:
            {
                "basic_saju": {...},        # 기본 사주팔자
                "daeun": {...},             # 대운
                "seun": {...},              # 세운
                "hyeongchung": {...},       # 형충회합
                "sibiunseong": {...},       # 십이운성
                "sinsal": {...}             # 신살
            }
        """
        # 1. 기본 사주팔자 계산
        basic_saju = self.saju_calculator.calculate(
            birth_date=birth_date,
            birth_location=birth_location,
            is_lunar=is_lunar,
            is_leap_month=is_leap_month
        )

        # 기둥 정보 추출
        pillars = basic_saju["pillars"]
        year_pillar = pillars["year"]
        month_pillar = pillars["month"]
        day_pillar = pillars["day"]
        hour_pillar = pillars["hour"]

        # CheonGan, JiJi 객체 재구성 (from dict)
        from .gapja import GapJa

        # 년주
        year_gan_idx = self._find_gan_index(year_pillar["gan"]["korean"])
        year_ji_idx = self._find_ji_index(year_pillar["ji"]["korean"])
        year_gan = GapJa.get_cheongan(year_gan_idx)
        year_ji = GapJa.get_jiji(year_ji_idx)

        # 월주
        month_gan_idx = self._find_gan_index(month_pillar["gan"]["korean"])
        month_ji_idx = self._find_ji_index(month_pillar["ji"]["korean"])
        month_gan = GapJa.get_cheongan(month_gan_idx)
        month_ji = GapJa.get_jiji(month_ji_idx)

        # 일주
        day_gan_idx = self._find_gan_index(day_pillar["gan"]["korean"])
        day_ji_idx = self._find_ji_index(day_pillar["ji"]["korean"])
        day_gan = GapJa.get_cheongan(day_gan_idx)
        day_ji = GapJa.get_jiji(day_ji_idx)

        # 시주
        hour_gan_idx = self._find_gan_index(hour_pillar["gan"]["korean"])
        hour_ji_idx = self._find_ji_index(hour_pillar["ji"]["korean"])
        hour_gan = GapJa.get_cheongan(hour_gan_idx)
        hour_ji = GapJa.get_jiji(hour_ji_idx)

        # 2. 대운 계산
        daeun_start_age, daeun_pillars = DaeunCalculator.calculate(
            birth_date=birth_date,
            year_gan=year_gan,
            month_gan=month_gan,
            month_ji=month_ji,
            gender=gender
        )

        daeun_result = {
            "start_age": daeun_start_age,
            "pillars": [p.to_dict() for p in daeun_pillars]
        }

        # 현재 대운 추가
        if current_age:
            current_daeun = DaeunCalculator.get_current_daeun(daeun_pillars, current_age)
            daeun_result["current"] = current_daeun.to_dict() if current_daeun else None

        # 3. 세운 계산 (target_year 제공 시)
        seun_result = None
        if target_year:
            seun_year_gan, seun_year_ji = SeunCalculator.get_year_fortune(target_year)

            seun_result = {
                "target_year": target_year,
                "year_gan": seun_year_gan.korean,
                "year_ji": seun_year_ji.korean,
                "combined": f"{seun_year_gan.korean}{seun_year_ji.korean}",
                "hanja": f"{seun_year_gan.hanja}{seun_year_ji.hanja}"
            }

            # 대운과 세운의 상호작용 (현재 나이 제공 시)
            if current_age and daeun_result.get("current"):
                current_daeun_dict = daeun_result["current"]
                # 대운 간지 재구성
                daeun_gan_idx = self._find_gan_index(current_daeun_dict["gan"]["korean"])
                daeun_ji_idx = self._find_ji_index(current_daeun_dict["ji"]["korean"])
                daeun_gan = GapJa.get_cheongan(daeun_gan_idx)
                daeun_ji = GapJa.get_jiji(daeun_ji_idx)

                interaction = SeunCalculator.analyze_fortune_interaction(
                    saju_day_gan=day_gan,
                    daeun_gan=daeun_gan,
                    daeun_ji=daeun_ji,
                    seun_gan=seun_year_gan,
                    seun_ji=seun_year_ji
                )
                seun_result["interaction"] = interaction

        # 4. 형충회합 분석
        hyeongchung_result = HyeongchungAnalyzer.analyze_saju(
            year_gan, year_ji,
            month_gan, month_ji,
            day_gan, day_ji,
            hour_gan, hour_ji
        )

        # 5. 십이운성 분석
        sibiunseong_result = SibiUnseong.analyze_saju_unseong(
            day_gan,
            year_ji, month_ji, day_ji, hour_ji
        )

        # 6. 신살 분석
        sinsal_result = Sinsal.analyze_all_sinsal(
            day_gan,
            year_ji, month_ji, day_ji, hour_ji
        )

        # 7. 종합 결과 반환
        return {
            "basic_saju": basic_saju,
            "daeun": daeun_result,
            "seun": seun_result,
            "hyeongchung": hyeongchung_result,
            "sibiunseong": sibiunseong_result,
            "sinsal": sinsal_result,
            "meta": {
                "calculated_at": datetime.now().isoformat(),
                "gender": gender,
                "is_deterministic": True,  # 결정론적 계산임을 명시
                "version": "1.0.0"
            }
        }

    def _find_gan_index(self, korean: str) -> int:
        """한글 천간으로 인덱스 찾기"""
        gan_map = {
            "갑": 0, "을": 1, "병": 2, "정": 3, "무": 4,
            "기": 5, "경": 6, "신": 7, "임": 8, "계": 9
        }
        return gan_map.get(korean, 0)

    def _find_ji_index(self, korean: str) -> int:
        """한글 지지로 인덱스 찾기"""
        ji_map = {
            "자": 0, "축": 1, "인": 2, "묘": 3, "진": 4, "사": 5,
            "오": 6, "미": 7, "신": 8, "유": 9, "술": 10, "해": 11
        }
        return ji_map.get(korean, 0)

    def format_for_ai_agent(self, manseryeok_result: Dict) -> str:
        """
        만세력 결과를 AI 에이전트용 텍스트로 포맷

        이 텍스트를 AI 에이전트에게 전달하여 해석을 받음
        """
        basic = manseryeok_result["basic_saju"]
        daeun = manseryeok_result["daeun"]
        hyeongchung = manseryeok_result["hyeongchung"]
        sibiunseong = manseryeok_result["sibiunseong"]
        sinsal = manseryeok_result["sinsal"]

        formatted = f"""
# 만세력 분석 데이터

## 기본 사주팔자
{basic['summary']}

**사주 구조:**
```
{basic['pillars']['hour']['combined']}  {basic['pillars']['day']['combined']}  {basic['pillars']['month']['combined']}  {basic['pillars']['year']['combined']}
시주        일주        월주        년주
```

## 오행 분석
- 오행 개수: {basic['element_analysis']['element_count']}
- 일간: {basic['element_analysis']['day_master']}
- 최강: {basic['element_analysis']['strongest']}
- 최약: {basic['element_analysis']['weakest']}

## 대운 (大運)
- 대운 시작: {daeun['start_age']}세
- 대운 목록:
"""

        for pillar in daeun['pillars'][:5]:  # 처음 5개만
            formatted += f"  * {pillar['age_range']}: {pillar['combined']} ({pillar['hanja']})\n"

        if daeun.get('current'):
            current_daeun = daeun['current']
            formatted += f"\n**현재 대운:** {current_daeun['age_range']} - {current_daeun['combined']}\n"

        formatted += f"""
## 형충회합
{hyeongchung['summary']}

"""

        if hyeongchung['cheongan_relations']:
            formatted += "**천간 관계:**\n"
            for rel in hyeongchung['cheongan_relations']:
                formatted += f"- {rel['type']}: {rel['detail']} ({rel['impact']})\n"

        if hyeongchung['jiji_relations']:
            formatted += "\n**지지 관계:**\n"
            for rel in hyeongchung['jiji_relations'][:5]:  # 처음 5개만
                formatted += f"- {rel['type']}: {rel['detail']} ({rel['impact']})\n"

        formatted += f"""
## 십이운성
{sibiunseong['summary']}

- 년지: {sibiunseong['year']['unseong']}
- 월지: {sibiunseong['month']['unseong']}
- 일지: {sibiunseong['day']['unseong']}
- 시지: {sibiunseong['hour']['unseong']}

## 신살
{sinsal['summary']['description']}

"""

        if sinsal['summary']['good']:
            formatted += f"**길신:** {', '.join(sinsal['summary']['good'])}\n"

        if sinsal['summary']['bad']:
            formatted += f"**흉신:** {', '.join(sinsal['summary']['bad'])}\n"

        return formatted


# 편의 함수
def calculate_manseryeok(
    birth_date: datetime,
    gender: str,
    birth_location: Optional[str] = None,
    is_lunar: bool = False,
    current_age: Optional[int] = None,
    target_year: Optional[int] = None
) -> Dict:
    """
    만세력 계산 편의 함수

    Example:
        >>> from datetime import datetime
        >>> result = calculate_manseryeok(
        ...     birth_date=datetime(1990, 5, 15, 14, 30),
        ...     gender="남",
        ...     birth_location="서울",
        ...     current_age=35,
        ...     target_year=2025
        ... )
    """
    manseryeok = Manseryeok()
    return manseryeok.calculate_full(
        birth_date=birth_date,
        gender=gender,
        birth_location=birth_location,
        is_lunar=is_lunar,
        current_age=current_age,
        target_year=target_year
    )
