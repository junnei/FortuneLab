"""
대운(大運) 계산 모듈
10년 주기로 바뀌는 운세

자평명리학에서 대운은:
- 양남음녀(陽男陰女): 월주에서 순행(順行)
- 음남양녀(陰男陽女): 월주에서 역행(逆行)
- 대운 시작 나이는 생일부터 다음/이전 절기까지의 일수로 계산
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from .gapja import GapJa, CheonGan, JiJi
from .solar_terms import SolarTerms


class DaeunPillar:
    """대운 한 기둥"""

    def __init__(
        self,
        gan: CheonGan,
        ji: JiJi,
        start_age: int,
        end_age: int
    ):
        self.gan = gan
        self.ji = ji
        self.start_age = start_age
        self.end_age = end_age

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
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
            "hanja": f"{self.gan.hanja}{self.ji.hanja}",
            "age_range": f"{self.start_age}~{self.end_age}세"
        }

    def __repr__(self):
        return f"{self.start_age}~{self.end_age}세: {self.gan.korean}{self.ji.korean}"


class DaeunCalculator:
    """대운 계산기"""

    @classmethod
    def calculate(
        cls,
        birth_date: datetime,
        year_gan: CheonGan,
        month_gan: CheonGan,
        month_ji: JiJi,
        gender: str  # "남" 또는 "여"
    ) -> Tuple[int, List[DaeunPillar]]:
        """
        대운 계산

        Args:
            birth_date: 생년월일시
            year_gan: 년간
            month_gan: 월간
            month_ji: 월지
            gender: 성별 ("남" 또는 "여")

        Returns:
            (대운 시작 나이, 대운 목록)
        """
        # 1. 순행/역행 결정
        is_forward = cls._determine_direction(year_gan, gender)

        # 2. 대운 시작 나이 계산
        start_age = cls._calculate_start_age(birth_date, is_forward)

        # 3. 대운 기둥들 생성 (보통 8~10개 계산)
        daeun_pillars = cls._generate_daeun_pillars(
            month_gan,
            month_ji,
            start_age,
            is_forward,
            num_pillars=10
        )

        return start_age, daeun_pillars

    @classmethod
    def _determine_direction(cls, year_gan: CheonGan, gender: str) -> bool:
        """
        대운 순행/역행 결정

        - 양남음녀(陽男陰女): 순행 (True)
        - 음남양녀(陰男陽女): 역행 (False)

        Args:
            year_gan: 년간
            gender: 성별 ("남" 또는 "여")

        Returns:
            True면 순행, False면 역행
        """
        is_yang_gan = year_gan.polarity == "+"

        if gender == "남":
            return is_yang_gan  # 양남은 순행, 음남은 역행
        else:  # 여
            return not is_yang_gan  # 음녀는 순행, 양녀는 역행

    @classmethod
    def _calculate_start_age(cls, birth_date: datetime, is_forward: bool) -> int:
        """
        대운 시작 나이 계산

        순행: 생일부터 다음 절기까지 일수
        역행: 생일부터 이전 절기까지 일수

        일수를 3으로 나누어 1년으로 환산 (3일 = 1년)

        Args:
            birth_date: 생년월일
            is_forward: 순행 여부

        Returns:
            대운 시작 나이
        """
        year = birth_date.year

        # 현재 절기 찾기
        if year in SolarTerms.SOLAR_TERM_DATES:
            year_terms = SolarTerms.SOLAR_TERM_DATES[year]

            # 주요 절기들 (월 시작 기준)
            major_terms = ["입춘", "경칩", "청명", "입하", "망종", "소서",
                          "입추", "백로", "한로", "입동", "대설", "소한"]

            if is_forward:
                # 다음 절기까지 일수
                next_term_date = None
                for term in major_terms:
                    if term in year_terms and year_terms[term] > birth_date:
                        next_term_date = year_terms[term]
                        break

                # 다음 해 절기 확인
                if next_term_date is None and (year + 1) in SolarTerms.SOLAR_TERM_DATES:
                    next_year_terms = SolarTerms.SOLAR_TERM_DATES[year + 1]
                    if "입춘" in next_year_terms:
                        next_term_date = next_year_terms["입춘"]

                if next_term_date:
                    days_diff = (next_term_date - birth_date).days
                else:
                    days_diff = 90  # 기본값

            else:  # 역행
                # 이전 절기까지 일수
                prev_term_date = None
                for term in reversed(major_terms):
                    if term in year_terms and year_terms[term] < birth_date:
                        prev_term_date = year_terms[term]
                        break

                # 이전 해 절기 확인
                if prev_term_date is None and (year - 1) in SolarTerms.SOLAR_TERM_DATES:
                    prev_year_terms = SolarTerms.SOLAR_TERM_DATES[year - 1]
                    if "대설" in prev_year_terms:
                        prev_term_date = prev_year_terms["대설"]

                if prev_term_date:
                    days_diff = (birth_date - prev_term_date).days
                else:
                    days_diff = 90  # 기본값

            # 3일 = 1년 환산
            start_age = days_diff // 3
            if start_age == 0:
                start_age = 1  # 최소 1세
        else:
            # 절기 데이터 없으면 대략적 계산
            start_age = cls._approximate_start_age(birth_date, is_forward)

        return start_age

    @classmethod
    def _approximate_start_age(cls, birth_date: datetime, is_forward: bool) -> int:
        """절기 데이터 없을 때 대략적인 대운 시작 나이 계산"""
        # 간단한 근사: 생일 날짜를 기준으로 계산
        if is_forward:
            # 다음 절기까지 대략 계산
            days_to_next = 45 - (birth_date.day % 45)
        else:
            # 이전 절기까지 대략 계산
            days_to_prev = birth_date.day % 45

        days_diff = days_to_next if is_forward else days_to_prev
        start_age = max(1, days_diff // 3)

        return start_age

    @classmethod
    def _generate_daeun_pillars(
        cls,
        month_gan: CheonGan,
        month_ji: JiJi,
        start_age: int,
        is_forward: bool,
        num_pillars: int = 10
    ) -> List[DaeunPillar]:
        """
        대운 기둥들 생성

        월주에서 시작하여 순행 또는 역행

        Args:
            month_gan: 월간
            month_ji: 월지
            start_age: 대운 시작 나이
            is_forward: 순행 여부
            num_pillars: 생성할 대운 개수

        Returns:
            대운 기둥 리스트
        """
        pillars = []
        current_gan_index = month_gan.index
        current_ji_index = month_ji.index
        current_age = start_age

        for i in range(num_pillars):
            # 첫 번째 대운은 월주의 다음/이전
            if is_forward:
                gan_index = (current_gan_index + i + 1) % 10
                ji_index = (current_ji_index + i + 1) % 12
            else:
                gan_index = (current_gan_index - i - 1) % 10
                ji_index = (current_ji_index - i - 1) % 12

            gan = GapJa.get_cheongan(gan_index)
            ji = GapJa.get_jiji(ji_index)

            age_start = current_age + (i * 10)
            age_end = age_start + 9

            pillar = DaeunPillar(gan, ji, age_start, age_end)
            pillars.append(pillar)

        return pillars

    @classmethod
    def get_current_daeun(
        cls,
        daeun_pillars: List[DaeunPillar],
        current_age: int
    ) -> DaeunPillar:
        """현재 나이의 대운 반환"""
        for pillar in daeun_pillars:
            if pillar.start_age <= current_age <= pillar.end_age:
                return pillar

        # 범위 밖이면 가장 가까운 대운 반환
        if current_age < daeun_pillars[0].start_age:
            return daeun_pillars[0]
        else:
            return daeun_pillars[-1]


class SeunCalculator:
    """세운(歲運) 계산기 - 년운, 월운"""

    @classmethod
    def get_year_fortune(cls, target_year: int) -> Tuple[CheonGan, JiJi]:
        """
        특정 년도의 세운(년주) 반환

        Args:
            target_year: 대상 년도 (예: 2025)

        Returns:
            (천간, 지지) 튜플
        """
        return GapJa.get_year_gapja(target_year)

    @classmethod
    def get_month_fortune(
        cls,
        target_date: datetime,
        year_gan_index: int
    ) -> Tuple[CheonGan, JiJi]:
        """
        특정 월의 세운(월주) 반환

        Args:
            target_date: 대상 날짜
            year_gan_index: 해당 년도의 년간 인덱스

        Returns:
            (천간, 지지) 튜플
        """
        return GapJa.get_month_gapja(year_gan_index, target_date.month)

    @classmethod
    def analyze_fortune_interaction(
        cls,
        saju_day_gan: CheonGan,
        daeun_gan: CheonGan,
        daeun_ji: JiJi,
        seun_gan: CheonGan,
        seun_ji: JiJi
    ) -> Dict:
        """
        사주 일간과 대운, 세운의 상호작용 분석

        Args:
            saju_day_gan: 사주 일간
            daeun_gan: 대운 천간
            daeun_ji: 대운 지지
            seun_gan: 세운 천간
            seun_ji: 세운 지지

        Returns:
            분석 결과 딕셔너리
        """
        from .gapja import OHaeng

        day_element = saju_day_gan.element

        return {
            "daeun_gan_relation": OHaeng.get_relation(day_element, daeun_gan.element),
            "daeun_ji_relation": OHaeng.get_relation(day_element, daeun_ji.element),
            "seun_gan_relation": OHaeng.get_relation(day_element, seun_gan.element),
            "seun_ji_relation": OHaeng.get_relation(day_element, seun_ji.element),
            "summary": cls._generate_interaction_summary(
                day_element,
                daeun_gan.element,
                seun_gan.element
            )
        }

    @classmethod
    def _generate_interaction_summary(
        cls,
        day_element: str,
        daeun_element: str,
        seun_element: str
    ) -> str:
        """상호작용 요약 생성"""
        from .gapja import OHaeng

        daeun_rel = OHaeng.get_relation(day_element, daeun_element)
        seun_rel = OHaeng.get_relation(day_element, seun_element)

        summary = f"대운: {daeun_rel}, 세운: {seun_rel}"

        # 길흉 판단
        if "관성" in daeun_rel or "인성" in daeun_rel:
            summary += " - 대운이 유리합니다."
        elif "재성" in daeun_rel or "식상" in daeun_rel:
            summary += " - 대운에 주의가 필요합니다."

        return summary
