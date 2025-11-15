"""
24절기 (Solar Terms) 계산 모듈
자평명리학에서 월주는 절기를 기준으로 결정됨
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json


class SolarTerms:
    """24절기 계산 클래스"""

    # 24절기 정의 (순서대로)
    TERMS = [
        "소한",  # 0  - 1월 (소한-입춘 사이: 축월)
        "입춘",  # 1  - 2월 시작 (인월)
        "우수",  # 2
        "경칩",  # 3  - 3월 시작 (묘월)
        "춘분",  # 4
        "청명",  # 5  - 4월 시작 (진월)
        "곡우",  # 6
        "입하",  # 7  - 5월 시작 (사월)
        "소만",  # 8
        "망종",  # 9  - 6월 시작 (오월)
        "하지",  # 10
        "소서",  # 11 - 7월 시작 (미월)
        "대서",  # 12
        "입추",  # 13 - 8월 시작 (신월)
        "처서",  # 14
        "백로",  # 15 - 9월 시작 (유월)
        "추분",  # 16
        "한로",  # 17 - 10월 시작 (술월)
        "상강",  # 18
        "입동",  # 19 - 11월 시작 (해월)
        "소설",  # 20
        "대설",  # 21 - 12월 시작 (자월)
        "동지",  # 22
        "소한",  # 23 - 다음해 1월 (축월)
    ]

    # 절기에 따른 월지 매핑 (사주 월 결정)
    TERM_TO_MONTH_JI = {
        "소한": 1,   # 축월 (丑)
        "입춘": 2,   # 인월 (寅) - 새해 시작
        "경칩": 3,   # 묘월 (卯)
        "청명": 4,   # 진월 (辰)
        "입하": 5,   # 사월 (巳)
        "망종": 6,   # 오월 (午)
        "소서": 7,   # 미월 (未)
        "입추": 8,   # 신월 (申)
        "백로": 9,   # 유월 (酉)
        "한로": 10,  # 술월 (戌)
        "입동": 11,  # 해월 (亥)
        "대설": 12,  # 자월 (子)
    }

    # 2020-2030년 주요 절기 절입시각 (KST 기준)
    # 실제로는 천문대 데이터 또는 정밀 계산 필요
    SOLAR_TERM_DATES = {
        2024: {
            "입춘": datetime(2024, 2, 4, 17, 27),
            "경칩": datetime(2024, 3, 5, 11, 23),
            "청명": datetime(2024, 4, 4, 16, 2),
            "입하": datetime(2024, 5, 5, 9, 10),
            "망종": datetime(2024, 6, 5, 13, 10),
            "소서": datetime(2024, 7, 6, 23, 20),
            "입추": datetime(2024, 8, 7, 15, 9),
            "백로": datetime(2024, 9, 7, 12, 11),
            "한로": datetime(2024, 10, 8, 3, 0),
            "입동": datetime(2024, 11, 7, 1, 20),
            "대설": datetime(2024, 12, 6, 18, 17),
            "소한": datetime(2024, 1, 6, 5, 49),
        },
        2025: {
            "입춘": datetime(2025, 2, 3, 23, 10),
            "경칩": datetime(2025, 3, 5, 17, 7),
            "청명": datetime(2025, 4, 4, 21, 48),
            "입하": datetime(2025, 5, 5, 14, 56),
            "망종": datetime(2025, 6, 5, 18, 57),
            "소서": datetime(2025, 7, 7, 5, 5),
            "입추": datetime(2025, 8, 7, 20, 52),
            "백로": datetime(2025, 9, 7, 17, 52),
            "한로": datetime(2025, 10, 8, 8, 42),
            "입동": datetime(2025, 11, 7, 7, 4),
            "대설": datetime(2025, 12, 7, 0, 5),
            "소한": datetime(2025, 1, 5, 11, 32),
        },
    }

    @classmethod
    def get_saju_month_ji_index(cls, birth_date: datetime, year: int) -> int:
        """
        절기 기준으로 사주 월지 인덱스 반환

        Args:
            birth_date: 태어난 날짜시간 (KST)
            year: 년도

        Returns:
            월지 인덱스 (0=자, 1=축, 2=인, ...)
        """
        if year not in cls.SOLAR_TERM_DATES:
            # 데이터가 없는 경우 대략적인 계산
            return cls._approximate_month_ji(birth_date)

        year_terms = cls.SOLAR_TERM_DATES[year]

        # 현재 시점이 어느 절기 이후인지 확인
        month_ji = 1  # 기본값: 축월 (소한 이후)

        for term in ["입춘", "경칩", "청명", "입하", "망종", "소서",
                     "입추", "백로", "한로", "입동", "대설"]:
            if term in year_terms and birth_date >= year_terms[term]:
                month_ji = cls.TERM_TO_MONTH_JI[term]

        # 소한 처리 (해를 넘어갈 수 있음)
        if "소한" in year_terms:
            if birth_date.month == 1 and birth_date < year_terms.get("입춘", datetime(year, 2, 4)):
                # 1월이고 입춘 전이면 축월
                month_ji = 1

        return month_ji

    @classmethod
    def _approximate_month_ji(cls, birth_date: datetime) -> int:
        """
        절기 데이터가 없을 때 대략적인 월지 계산
        (정확도는 떨어지지만 근사값 제공)
        """
        # 대략적인 절기 시작일 (매년 비슷함)
        approximate_terms = {
            2: 4,   # 입춘: 2월 4일경 -> 인월(2)
            3: 6,   # 경칩: 3월 6일경 -> 묘월(3)
            4: 5,   # 청명: 4월 5일경 -> 진월(4)
            5: 6,   # 입하: 5월 6일경 -> 사월(5)
            6: 6,   # 망종: 6월 6일경 -> 오월(6)
            7: 7,   # 소서: 7월 7일경 -> 미월(7)
            8: 8,   # 입추: 8월 8일경 -> 신월(8)
            9: 8,   # 백로: 9월 8일경 -> 유월(9)
            10: 8,  # 한로: 10월 8일경 -> 술월(10)
            11: 7,  # 입동: 11월 7일경 -> 해월(11)
            12: 7,  # 대설: 12월 7일경 -> 자월(0)
            1: 6,   # 소한: 1월 6일경 -> 축월(1)
        }

        month = birth_date.month
        day = birth_date.day

        if month == 1:
            return 1 if day >= approximate_terms[1] else 0
        elif month == 12:
            return 0 if day >= approximate_terms[12] else 11
        else:
            term_day = approximate_terms.get(month, 6)
            if day >= term_day:
                # 절기 이후
                return (month % 12) + 1
            else:
                # 절기 이전
                return month % 12

    @classmethod
    def get_current_term(cls, date: datetime, year: int) -> Optional[str]:
        """현재 날짜의 절기 반환"""
        if year not in cls.SOLAR_TERM_DATES:
            return None

        year_terms = cls.SOLAR_TERM_DATES[year]
        current_term = "소한"  # 기본값

        for term, term_date in sorted(year_terms.items(), key=lambda x: x[1]):
            if date >= term_date:
                current_term = term

        return current_term

    @classmethod
    def is_after_term(cls, date: datetime, term_name: str, year: int) -> bool:
        """특정 절기 이후인지 확인"""
        if year not in cls.SOLAR_TERM_DATES:
            return False

        term_date = cls.SOLAR_TERM_DATES[year].get(term_name)
        if term_date is None:
            return False

        return date >= term_date

    @classmethod
    def add_solar_term_data(cls, year: int, terms_data: Dict[str, datetime]):
        """새로운 년도의 절기 데이터 추가"""
        cls.SOLAR_TERM_DATES[year] = terms_data
