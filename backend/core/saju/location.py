"""
출생 장소 기반 경도 보정 및 시간 계산 모듈
진태양시 (Local Mean Time) 계산
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz


class LocationTimeCalculator:
    """출생 장소 기반 시간 계산 클래스"""

    # 한국 표준시 기준 경도 (동경 135도)
    STANDARD_LONGITUDE = 135.0

    # 서울 기준 경도 (동경 127.0)
    SEOUL_LONGITUDE = 127.0

    # 경도 1도당 시간 차이 (4분)
    MINUTES_PER_DEGREE = 4

    def __init__(self):
        self.geolocator = Nominatim(user_agent="fortune-lab")
        self.tf = TimezoneFinder()

    def get_coordinates(self, location_name: str) -> Optional[Tuple[float, float]]:
        """
        장소 이름으로 위도/경도 조회

        Args:
            location_name: 장소 이름 (예: "서울특별시", "부산광역시", "Seoul, South Korea")

        Returns:
            (위도, 경도) 튜플 또는 None
        """
        try:
            location = self.geolocator.geocode(location_name)
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception as e:
            print(f"위치 조회 오류: {e}")
            return None

    def calculate_longitude_correction(self, longitude: float) -> int:
        """
        경도 차이에 따른 시간 보정값 계산 (분 단위)

        한국 표준시는 동경 135도 기준이므로,
        실제 경도와의 차이만큼 시간을 보정해야 함

        Args:
            longitude: 출생지 경도

        Returns:
            보정 시간 (분) - 양수는 더해야 함, 음수는 빼야 함
        """
        # 경도 차이 계산
        longitude_diff = self.STANDARD_LONGITUDE - longitude

        # 경도 1도당 4분 차이
        correction_minutes = int(longitude_diff * self.MINUTES_PER_DEGREE)

        return correction_minutes

    def get_solar_time(
        self,
        birth_datetime: datetime,
        longitude: float,
        apply_dst: bool = True
    ) -> datetime:
        """
        진태양시 계산

        Args:
            birth_datetime: 출생 일시 (KST)
            longitude: 출생지 경도
            apply_dst: 서머타임 적용 여부

        Returns:
            진태양시로 보정된 datetime
        """
        # 경도 보정
        correction_minutes = self.calculate_longitude_correction(longitude)
        solar_time = birth_datetime - timedelta(minutes=correction_minutes)

        # 서머타임 보정 (한국은 1948-1960년, 1987-1988년에 사용)
        if apply_dst and self._is_dst_period(birth_datetime):
            solar_time = solar_time - timedelta(hours=1)

        return solar_time

    def _is_dst_period(self, dt: datetime) -> bool:
        """
        서머타임 적용 기간인지 확인

        한국 서머타임 적용 기간:
        - 1948-1951: 5월 첫째 일요일 ~ 9월 둘째 토요일
        - 1952-1960: 5월 첫째 일요일 ~ 9월 셋째 토요일
        - 1987-1988: 5월 10일 ~ 10월 11일
        """
        year = dt.year

        if 1948 <= year <= 1951:
            return 5 <= dt.month <= 9
        elif 1952 <= year <= 1960:
            return 5 <= dt.month <= 9
        elif 1987 <= year <= 1988:
            return (dt.month == 5 and dt.day >= 10) or \
                   (5 < dt.month < 10) or \
                   (dt.month == 10 and dt.day <= 11)
        return False

    def get_hour_for_saju(
        self,
        birth_datetime: datetime,
        location_name: Optional[str] = None,
        longitude: Optional[float] = None
    ) -> int:
        """
        사주 계산용 시간 반환 (진태양시 기준)

        Args:
            birth_datetime: 출생 일시 (KST)
            location_name: 출생지 이름 (예: "서울")
            longitude: 출생지 경도 (직접 제공 가능)

        Returns:
            보정된 시(hour) 값 (0-23)
        """
        # 경도 확인
        if longitude is None:
            if location_name:
                coords = self.get_coordinates(location_name)
                if coords:
                    longitude = coords[1]
                else:
                    # 기본값: 서울 경도
                    longitude = self.SEOUL_LONGITUDE
            else:
                longitude = self.SEOUL_LONGITUDE

        # 진태양시 계산
        solar_time = self.get_solar_time(birth_datetime, longitude)

        return solar_time.hour

    def adjust_for_midnight(
        self,
        hour: int,
        use_early_jasi: bool = True
    ) -> Tuple[int, int]:
        """
        자시(子時) 보정

        자시는 23시~01시이므로 특별 처리 필요
        - 조자시(早子時): 23시~24시 -> 다음 날 일주 사용
        - 야자시(夜子時): 00시~01시 -> 당일 일주 사용

        Args:
            hour: 시간 (0-23)
            use_early_jasi: True면 조자시 사용 (일반적)

        Returns:
            (보정된 hour, 일주 보정값: -1/0/+1)
        """
        day_adjustment = 0

        if hour == 23:
            # 23시는 조자시
            if use_early_jasi:
                day_adjustment = 1  # 다음 날 일주 사용
        elif hour == 0:
            # 00시는 야자시
            if not use_early_jasi:
                day_adjustment = -1  # 이전 날 일주 사용

        return hour, day_adjustment


# 주요 한국 도시 경도 데이터
MAJOR_KOREAN_CITIES = {
    "서울": 126.9780,
    "부산": 129.0756,
    "대구": 128.6014,
    "인천": 126.7052,
    "광주": 126.8526,
    "대전": 127.3845,
    "울산": 129.3114,
    "세종": 127.2890,
    "경기": 127.0000,
    "강원": 128.0000,
    "충북": 127.7000,
    "충남": 126.8000,
    "전북": 127.0000,
    "전남": 126.9000,
    "경북": 128.8000,
    "경남": 128.5000,
    "제주": 126.5312,
}


def get_longitude_by_city(city_name: str) -> float:
    """도시 이름으로 경도 반환"""
    # 도시 이름에서 키워드 추출
    for city, longitude in MAJOR_KOREAN_CITIES.items():
        if city in city_name:
            return longitude

    # 기본값: 서울
    return MAJOR_KOREAN_CITIES["서울"]
