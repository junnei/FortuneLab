"""
천간지지(天干地支) 60갑자 계산 모듈
자평명리학의 기본이 되는 천간(10개)과 지지(12개)의 조합
"""

from typing import Tuple, Dict, List
from enum import Enum


class CheonGan(Enum):
    """천간 (Heavenly Stems) - 10개"""
    GAP = (0, "갑", "甲", "木", "+")   # 양목
    EUL = (1, "을", "乙", "木", "-")   # 음목
    BYEONG = (2, "병", "丙", "火", "+")  # 양화
    JEONG = (3, "정", "丁", "火", "-")  # 음화
    MU = (4, "무", "戊", "土", "+")    # 양토
    GI = (5, "기", "己", "土", "-")    # 음토
    GYEONG = (6, "경", "庚", "金", "+")  # 양금
    SIN = (7, "신", "辛", "金", "-")   # 음금
    IM = (8, "임", "壬", "水", "+")    # 양수
    GYE = (9, "계", "癸", "水", "-")   # 음수

    def __init__(self, index, korean, hanja, element, polarity):
        self.index = index
        self.korean = korean
        self.hanja = hanja
        self.element = element  # 오행: 木火土金水
        self.polarity = polarity  # 음양: + (양), - (음)


class JiJi(Enum):
    """지지 (Earthly Branches) - 12개"""
    JA = (0, "자", "子", "水", "-", "쥐", 11)    # 음수, 23-01시
    CHUK = (1, "축", "丑", "土", "-", "소", 1)   # 음토, 01-03시
    IN = (2, "인", "寅", "木", "+", "호랑이", 3)  # 양목, 03-05시
    MYO = (3, "묘", "卯", "木", "-", "토끼", 5)   # 음목, 05-07시
    JIN = (4, "진", "辰", "土", "+", "용", 7)    # 양토, 07-09시
    SA = (5, "사", "巳", "火", "-", "뱀", 9)     # 음화, 09-11시
    O = (6, "오", "午", "火", "+", "말", 11)     # 양화, 11-13시
    MI = (7, "미", "未", "土", "-", "양", 13)    # 음토, 13-15시
    SHIN = (8, "신", "申", "金", "+", "원숭이", 15)  # 양금, 15-17시
    YU = (9, "유", "酉", "金", "-", "닭", 17)    # 음금, 17-19시
    SUL = (10, "술", "戌", "土", "+", "개", 19)  # 양토, 19-21시
    HAE = (11, "해", "亥", "水", "+", "돼지", 21)  # 양수, 21-23시

    def __init__(self, index, korean, hanja, element, polarity, animal, hour_start):
        self.index = index
        self.korean = korean
        self.hanja = hanja
        self.element = element
        self.polarity = polarity
        self.animal = animal
        self.hour_start = hour_start  # 시작 시각 (시)


class GapJa:
    """60갑자 계산 클래스"""

    # 60갑자 순서표
    SIXTY_GAPJA = [
        "갑자", "을축", "병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유",
        "갑술", "을해", "병자", "정축", "무인", "기묘", "경진", "신사", "임오", "계미",
        "갑신", "을유", "병술", "정해", "무자", "기축", "경인", "신묘", "임진", "계사",
        "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축", "임인", "계묘",
        "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축",
        "갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", "계해"
    ]

    @classmethod
    def get_cheongan(cls, index: int) -> CheonGan:
        """인덱스로 천간 반환"""
        return list(CheonGan)[index % 10]

    @classmethod
    def get_jiji(cls, index: int) -> JiJi:
        """인덱스로 지지 반환"""
        return list(JiJi)[index % 12]

    @classmethod
    def get_gapja(cls, index: int) -> Tuple[CheonGan, JiJi]:
        """60갑자 인덱스로 천간지지 쌍 반환"""
        return (cls.get_cheongan(index), cls.get_jiji(index))

    @classmethod
    def get_gapja_string(cls, index: int) -> str:
        """60갑자 인덱스로 갑자 문자열 반환"""
        return cls.SIXTY_GAPJA[index % 60]

    @classmethod
    def get_year_gapja(cls, year: int) -> Tuple[CheonGan, JiJi]:
        """
        년주 계산
        기준: 1984년 = 갑자년 (index 0)
        """
        # 1984년이 갑자년(0)이므로 이를 기준으로 계산
        index = (year - 1984) % 60
        return cls.get_gapja(index)

    @classmethod
    def get_month_gapja(cls, year_gan_index: int, solar_month: int) -> Tuple[CheonGan, JiJi]:
        """
        월주 계산
        월지는 절기를 기준으로 결정됨
        월간은 년간에 따라 정해짐 (오호송 구결)

        년간별 정월(인월) 월간:
        갑기년: 병인월로 시작
        을경년: 무인월로 시작
        병신년: 경인월로 시작
        정임년: 임인월로 시작
        무계년: 갑인월로 시작
        """
        # 월지 결정 (인묘진사오미신유술해자축)
        # 음력 1월=인, 2월=묘, 3월=진...
        month_jiji_map = {
            2: 2,   # 입춘-경칩: 인월(寅)
            3: 3,   # 경칩-청명: 묘월(卯)
            4: 4,   # 청명-입하: 진월(辰)
            5: 5,   # 입하-망종: 사월(巳)
            6: 6,   # 망종-소서: 오월(午)
            7: 7,   # 소서-입추: 미월(未)
            8: 8,   # 입추-백로: 신월(申)
            9: 9,   # 백로-한로: 유월(酉)
            10: 10, # 한로-입동: 술월(戌)
            11: 11, # 입동-대설: 해월(亥)
            12: 0,  # 대설-소한: 자월(子)
            1: 1,   # 소한-입춘: 축월(丑)
        }

        month_jiji_index = month_jiji_map.get(solar_month, 2)

        # 월간 결정 (오호송 구결)
        year_gan_mod = year_gan_index % 5
        month_gan_start = {
            0: 2,  # 갑, 기: 병인월로 시작
            1: 4,  # 을, 경: 무인월로 시작
            2: 6,  # 병, 신: 경인월로 시작
            3: 8,  # 정, 임: 임인월로 시작
            4: 0,  # 무, 계: 갑인월로 시작
        }

        # 인월(index 2)을 기준으로 계산
        base_month = 2  # 정월=인월
        month_offset = (month_jiji_index - base_month) % 12
        month_gan_index = (month_gan_start[year_gan_mod] + month_offset) % 10

        return (cls.get_cheongan(month_gan_index), cls.get_jiji(month_jiji_index))

    @classmethod
    def get_hour_gapja(cls, day_gan_index: int, hour: int) -> Tuple[CheonGan, JiJi]:
        """
        시주 계산
        시지는 시간으로 결정
        시간은 일간에 따라 정해짐 (오자시송)

        일간별 자시(23-01시) 시간:
        갑기일: 갑자시로 시작
        을경일: 병자시로 시작
        병신일: 무자시로 시작
        정임일: 경자시로 시작
        무계일: 임자시로 시작
        """
        # 시지 결정
        if 23 <= hour or hour < 1:
            hour_jiji_index = 0  # 자시
        elif 1 <= hour < 3:
            hour_jiji_index = 1  # 축시
        elif 3 <= hour < 5:
            hour_jiji_index = 2  # 인시
        elif 5 <= hour < 7:
            hour_jiji_index = 3  # 묘시
        elif 7 <= hour < 9:
            hour_jiji_index = 4  # 진시
        elif 9 <= hour < 11:
            hour_jiji_index = 5  # 사시
        elif 11 <= hour < 13:
            hour_jiji_index = 6  # 오시
        elif 13 <= hour < 15:
            hour_jiji_index = 7  # 미시
        elif 15 <= hour < 17:
            hour_jiji_index = 8  # 신시
        elif 17 <= hour < 19:
            hour_jiji_index = 9  # 유시
        elif 19 <= hour < 21:
            hour_jiji_index = 10  # 술시
        else:  # 21 <= hour < 23
            hour_jiji_index = 11  # 해시

        # 시간 결정 (오자시송)
        day_gan_mod = day_gan_index % 5
        hour_gan_start = {
            0: 0,  # 갑, 기: 갑자시로 시작
            1: 2,  # 을, 경: 병자시로 시작
            2: 4,  # 병, 신: 무자시로 시작
            3: 6,  # 정, 임: 경자시로 시작
            4: 8,  # 무, 계: 임자시로 시작
        }

        hour_gan_index = (hour_gan_start[day_gan_mod] + hour_jiji_index) % 10

        return (cls.get_cheongan(hour_gan_index), cls.get_jiji(hour_jiji_index))


class OHaeng:
    """오행(五行) 관계 분석 클래스"""

    # 오행 상생 관계: 木生火, 火生土, 土生金, 金生水, 水生木
    SAENG = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木"
    }

    # 오행 상극 관계: 木克土, 土克水, 水克火, 火克金, 金克木
    GEUK = {
        "木": "土",
        "土": "水",
        "水": "火",
        "火": "金",
        "金": "木"
    }

    @classmethod
    def get_relation(cls, from_element: str, to_element: str) -> str:
        """두 오행 간의 관계 반환"""
        if from_element == to_element:
            return "비겁(比劫)"  # 같은 오행
        elif cls.SAENG.get(from_element) == to_element:
            return "식상(食傷)"  # 내가 생하는 것
        elif cls.SAENG.get(to_element) == from_element:
            return "인성(印星)"  # 나를 생하는 것
        elif cls.GEUK.get(from_element) == to_element:
            return "재성(財星)"  # 내가 극하는 것
        elif cls.GEUK.get(to_element) == from_element:
            return "관성(官星)"  # 나를 극하는 것
        return "알 수 없음"

    @classmethod
    def count_elements(cls, saju_pillars: List[Tuple[CheonGan, JiJi]]) -> Dict[str, int]:
        """사주팔자의 오행 개수 세기"""
        element_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

        for gan, ji in saju_pillars:
            element_count[gan.element] += 1
            element_count[ji.element] += 1

        return element_count

    @classmethod
    def get_strongest_element(cls, element_count: Dict[str, int]) -> str:
        """가장 강한 오행 반환"""
        return max(element_count, key=element_count.get)

    @classmethod
    def get_weakest_element(cls, element_count: Dict[str, int]) -> str:
        """가장 약한 오행 반환"""
        return min(element_count, key=element_count.get)
