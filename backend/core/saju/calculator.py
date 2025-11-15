"""
사주팔자 계산 핵심 모듈
생년월일시 + 출생지 -> 사주팔자 (년주, 월주, 일주, 시주)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from korean_lunar_calendar import KoreanLunarCalendar

from .gapja import GapJa, CheonGan, JiJi, OHaeng
from .solar_terms import SolarTerms
from .location import LocationTimeCalculator, get_longitude_by_city


class SajuPillar:
    """사주 한 기둥(柱) 데이터 클래스"""

    def __init__(
        self,
        gan: CheonGan,
        ji: JiJi,
        pillar_type: str  # "년주", "월주", "일주", "시주"
    ):
        self.gan = gan
        self.ji = ji
        self.pillar_type = pillar_type

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            "type": self.pillar_type,
            "gan": {
                "korean": self.gan.korean,
                "hanja": self.gan.hanja,
                "element": self.gan.element,
                "polarity": "양" if self.gan.polarity == "+" else "음"
            },
            "ji": {
                "korean": self.ji.korean,
                "hanja": self.ji.hanja,
                "element": self.ji.element,
                "polarity": "양" if self.ji.polarity == "+" else "음",
                "animal": self.ji.animal
            },
            "combined": f"{self.gan.korean}{self.ji.korean}",
            "hanja": f"{self.gan.hanja}{self.ji.hanja}"
        }

    def __repr__(self):
        return f"{self.pillar_type}: {self.gan.korean}{self.ji.korean}({self.gan.hanja}{self.ji.hanja})"


class SajuCalculator:
    """사주팔자 계산기"""

    def __init__(self):
        self.location_calculator = LocationTimeCalculator()

    def calculate(
        self,
        birth_date: datetime,
        birth_location: Optional[str] = None,
        is_lunar: bool = False,
        is_leap_month: bool = False,
        use_early_jasi: bool = True
    ) -> Dict:
        """
        사주팔자 계산

        Args:
            birth_date: 생년월일시 (datetime 객체)
            birth_location: 출생지 (예: "서울", "부산")
            is_lunar: 음력 여부
            is_leap_month: 윤달 여부 (음력인 경우만)
            use_early_jasi: 조자시 사용 여부 (23시를 다음날로 계산)

        Returns:
            사주팔자 정보 딕셔너리
        """
        # 1. 음력을 양력으로 변환 (필요시)
        solar_date = self._convert_to_solar(birth_date, is_lunar, is_leap_month)

        # 2. 출생지 경도 보정
        longitude = None
        if birth_location:
            longitude = get_longitude_by_city(birth_location)

        # 3. 진태양시 계산
        solar_hour = self.location_calculator.get_hour_for_saju(
            solar_date,
            birth_location,
            longitude
        )

        # 4. 자시 보정
        adjusted_hour, day_adjustment = self.location_calculator.adjust_for_midnight(
            solar_hour,
            use_early_jasi
        )

        # 일주 계산용 날짜 (자시 보정 적용)
        ilju_date = solar_date + timedelta(days=day_adjustment)

        # 5. 사주 사기둥 계산
        year_pillar = self._calculate_year_pillar(solar_date)
        month_pillar = self._calculate_month_pillar(solar_date, year_pillar)
        day_pillar = self._calculate_day_pillar(ilju_date)
        hour_pillar = self._calculate_hour_pillar(adjusted_hour, day_pillar)

        # 6. 오행 분석
        pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
        element_analysis = self._analyze_elements(pillars)

        # 7. 결과 반환
        return {
            "birth_info": {
                "solar_date": solar_date.strftime("%Y년 %m월 %d일 %H시"),
                "lunar_date": self._to_lunar_string(solar_date) if not is_lunar else None,
                "location": birth_location or "서울 (기본값)",
                "longitude_correction": f"{self.location_calculator.calculate_longitude_correction(longitude or 127.0)}분" if birth_location else "0분"
            },
            "pillars": {
                "year": year_pillar.to_dict(),
                "month": month_pillar.to_dict(),
                "day": day_pillar.to_dict(),
                "hour": hour_pillar.to_dict()
            },
            "element_analysis": element_analysis,
            "summary": self._generate_summary(pillars, element_analysis)
        }

    def _convert_to_solar(
        self,
        date: datetime,
        is_lunar: bool,
        is_leap_month: bool
    ) -> datetime:
        """음력을 양력으로 변환"""
        if not is_lunar:
            return date

        try:
            calendar = KoreanLunarCalendar()
            calendar.setLunarDate(
                date.year,
                date.month,
                date.day,
                is_leap_month
            )

            solar_year = calendar.solarYear
            solar_month = calendar.solarMonth
            solar_day = calendar.solarDay

            return datetime(
                solar_year,
                solar_month,
                solar_day,
                date.hour,
                date.minute
            )
        except Exception as e:
            print(f"음력 변환 오류: {e}")
            return date

    def _to_lunar_string(self, solar_date: datetime) -> str:
        """양력을 음력 문자열로 변환"""
        try:
            calendar = KoreanLunarCalendar()
            calendar.setSolarDate(
                solar_date.year,
                solar_date.month,
                solar_date.day
            )

            return f"{calendar.lunarYear}년 {calendar.lunarMonth}월 {calendar.lunarDay}일" + \
                   (" (윤달)" if calendar.isIntercalation else "")
        except:
            return "변환 불가"

    def _calculate_year_pillar(self, date: datetime) -> SajuPillar:
        """
        년주 계산
        입춘 기준으로 년도가 바뀜
        """
        year = date.year

        # 입춘 전이면 이전 해의 년주 사용
        if date.month <= 2:
            if not SolarTerms.is_after_term(date, "입춘", year):
                year -= 1

        gan, ji = GapJa.get_year_gapja(year)
        return SajuPillar(gan, ji, "년주")

    def _calculate_month_pillar(
        self,
        date: datetime,
        year_pillar: SajuPillar
    ) -> SajuPillar:
        """
        월주 계산
        24절기 기준으로 월이 결정됨
        """
        year = date.year
        month_ji_index = SolarTerms.get_saju_month_ji_index(date, year)

        # 년간을 기준으로 월간 계산
        year_gan_index = year_pillar.gan.index
        gan, ji = GapJa.get_month_gapja(year_gan_index, date.month)

        # 절기 기준 지지로 교체
        ji = GapJa.get_jiji(month_ji_index)

        return SajuPillar(gan, ji, "월주")

    def _calculate_day_pillar(self, date: datetime) -> SajuPillar:
        """
        일주 계산
        만세력 기준 일주 계산
        """
        try:
            calendar = KoreanLunarCalendar()
            calendar.setSolarDate(date.year, date.month, date.day)

            # korean-lunar-calendar 라이브러리의 간지 문자열 파싱
            gapja_string = calendar.getGapJaString()

            # "정유년 병오월 임오일" 형식에서 일주 추출
            parts = gapja_string.split()
            if len(parts) >= 3:
                day_gapja = parts[2].replace("일", "")

                # 간지 문자열에서 인덱스 찾기
                day_index = GapJa.SIXTY_GAPJA.index(day_gapja)
                gan, ji = GapJa.get_gapja(day_index)

                return SajuPillar(gan, ji, "일주")

        except Exception as e:
            print(f"일주 계산 오류: {e}")

        # 오류 시 간단한 계산 사용
        # 1900년 1월 1일 = 경자일(36)을 기준으로 계산
        base_date = datetime(1900, 1, 1)
        base_index = 36

        days_diff = (date - base_date).days
        day_index = (base_index + days_diff) % 60

        gan, ji = GapJa.get_gapja(day_index)
        return SajuPillar(gan, ji, "일주")

    def _calculate_hour_pillar(
        self,
        hour: int,
        day_pillar: SajuPillar
    ) -> SajuPillar:
        """시주 계산"""
        day_gan_index = day_pillar.gan.index
        gan, ji = GapJa.get_hour_gapja(day_gan_index, hour)

        return SajuPillar(gan, ji, "시주")

    def _analyze_elements(
        self,
        pillars: List[SajuPillar]
    ) -> Dict:
        """오행 분석"""
        # 오행 개수 세기
        gapja_pairs = [(p.gan, p.ji) for p in pillars]
        element_count = OHaeng.count_elements(gapja_pairs)

        # 일간 (자신)
        day_gan_element = pillars[2].gan.element

        # 각 기둥의 오행 관계
        relations = {}
        for pillar in pillars:
            gan_relation = OHaeng.get_relation(day_gan_element, pillar.gan.element)
            ji_relation = OHaeng.get_relation(day_gan_element, pillar.ji.element)

            relations[pillar.pillar_type] = {
                "gan": gan_relation,
                "ji": ji_relation
            }

        return {
            "element_count": element_count,
            "strongest": OHaeng.get_strongest_element(element_count),
            "weakest": OHaeng.get_weakest_element(element_count),
            "day_master": day_gan_element,
            "relations": relations
        }

    def _generate_summary(
        self,
        pillars: List[SajuPillar],
        element_analysis: Dict
    ) -> str:
        """사주 요약 생성"""
        summary_parts = []

        # 사주팔자 문자열
        saju_string = " ".join([
            f"{p.gan.korean}{p.ji.korean}" for p in pillars
        ])
        summary_parts.append(f"사주: {saju_string}")

        # 일간
        day_gan = pillars[2].gan
        summary_parts.append(f"일간: {day_gan.korean}({day_gan.hanja}) {day_gan.element}{'양' if day_gan.polarity == '+' else '음'}")

        # 오행 분포
        element_count = element_analysis["element_count"]
        element_str = ", ".join([f"{k}:{v}" for k, v in element_count.items()])
        summary_parts.append(f"오행: {element_str}")

        # 강약
        summary_parts.append(f"최강: {element_analysis['strongest']}, 최약: {element_analysis['weakest']}")

        return " | ".join(summary_parts)
