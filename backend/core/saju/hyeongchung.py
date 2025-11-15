"""
형충회합(刑沖會合) 분석 모듈

천간 합충:
- 천간오합(天干五合): 갑기합토, 을경합금, 병신합수, 정임합목, 무계합화
- 천간상충(天干相沖): 갑경충, 을신충, 병임충, 정계충

지지 합충형해파:
- 육합(六合): 자축합토, 인해합목, 묘술합화, 진유합금, 사신합수, 오미합화
- 삼합(三合): 신자진합수, 사유축합금, 인오술합화, 해묘미합목
- 방합(方合): 인묘진(동방목), 사오미(남방화), 신유술(서방금), 해자축(북방수)
- 육충(六沖): 자오충, 축미충, 인신충, 묘유충, 진술충, 사해충
- 삼형(三刑): 인사신(무은지형), 축술미(지세지형), 자묘(무례지형)
- 육해(六害): 자미해, 축오해, 인사해, 묘진해, 신해해, 유술해
- 육파(六破): 자유파, 오묘파, 진축파, 미술파, 인해파, 사신파
"""

from typing import List, Dict, Tuple, Set
from .gapja import CheonGan, JiJi


class CheonganRelation:
    """천간 관계 분석"""

    # 천간오합 (天干五合)
    OHAP = {
        (0, 4): ("갑기합토", "土"),  # 갑(0) + 기(5) -> 토
        (1, 6): ("을경합금", "金"),  # 을(1) + 경(6) -> 금
        (2, 7): ("병신합수", "水"),  # 병(2) + 신(7) -> 수
        (3, 8): ("정임합목", "木"),  # 정(3) + 임(8) -> 목
        (4, 9): ("무계합화", "火"),  # 무(4) + 계(9) -> 화
    }

    # 천간상충 (天干相沖)
    SANG_CHUNG = [
        (0, 6),  # 갑경충
        (1, 7),  # 을신충
        (2, 8),  # 병임충
        (3, 9),  # 정계충
    ]

    @classmethod
    def check_hap(cls, gan1: CheonGan, gan2: CheonGan) -> Tuple[bool, str, str]:
        """
        천간 합 체크

        Returns:
            (합 여부, 합 이름, 화합 오행)
        """
        idx1, idx2 = gan1.index, gan2.index
        key = tuple(sorted([idx1 % 5, idx2 % 5]))  # 0-4 범위로 정규화

        if key in cls.OHAP:
            hap_name, element = cls.OHAP[key]
            return True, hap_name, element

        return False, "", ""

    @classmethod
    def check_chung(cls, gan1: CheonGan, gan2: CheonGan) -> bool:
        """천간 충 체크"""
        idx1, idx2 = gan1.index, gan2.index
        key = tuple(sorted([idx1, idx2]))

        return key in cls.SANG_CHUNG


class JijiRelation:
    """지지 관계 분석"""

    # 육합 (六合)
    YUKHAP = {
        (0, 1): ("자축합토", "土"),   # 자 + 축 -> 토
        (2, 11): ("인해합목", "木"),  # 인 + 해 -> 목
        (3, 10): ("묘술합화", "火"),  # 묘 + 술 -> 화
        (4, 9): ("진유합금", "金"),   # 진 + 유 -> 금
        (5, 8): ("사신합수", "水"),   # 사 + 신 -> 수
        (6, 7): ("오미합화", "火"),   # 오 + 미 -> 화
    }

    # 삼합 (三合)
    SAMHAP = {
        frozenset([8, 0, 4]): ("신자진합수", "水"),  # 신 + 자 + 진
        frozenset([5, 9, 1]): ("사유축합금", "金"),  # 사 + 유 + 축
        frozenset([2, 6, 10]): ("인오술합화", "火"), # 인 + 오 + 술
        frozenset([11, 3, 7]): ("해묘미합목", "木"), # 해 + 묘 + 미
    }

    # 방합 (方合)
    BANGHAP = {
        frozenset([2, 3, 4]): ("인묘진 동방목", "木"),   # 인 + 묘 + 진
        frozenset([5, 6, 7]): ("사오미 남방화", "火"),   # 사 + 오 + 미
        frozenset([8, 9, 10]): ("신유술 서방금", "金"),  # 신 + 유 + 술
        frozenset([11, 0, 1]): ("해자축 북방수", "水"),  # 해 + 자 + 축
    }

    # 육충 (六沖)
    YUKCHUNG = [
        (0, 6),   # 자오충
        (1, 7),   # 축미충
        (2, 8),   # 인신충
        (3, 9),   # 묘유충
        (4, 10),  # 진술충
        (5, 11),  # 사해충
    ]

    # 삼형 (三刑)
    SAMHYEONG = [
        frozenset([2, 5, 8]),   # 인사신 (무은지형)
        frozenset([1, 4, 7]),   # 축술미 (지세지형)
        frozenset([0, 3]),      # 자묘 (무례지형)
    ]

    # 육해 (六害)
    YUKHAE = [
        (0, 7),   # 자미해
        (1, 6),   # 축오해
        (2, 5),   # 인사해
        (3, 4),   # 묘진해
        (8, 11),  # 신해해
        (9, 10),  # 유술해
    ]

    # 육파 (六破)
    YUKPA = [
        (0, 9),   # 자유파
        (6, 3),   # 오묘파
        (4, 1),   # 진축파
        (7, 10),  # 미술파
        (2, 11),  # 인해파
        (5, 8),   # 사신파
    ]

    @classmethod
    def check_yukhap(cls, ji1: JiJi, ji2: JiJi) -> Tuple[bool, str, str]:
        """육합 체크"""
        key = tuple(sorted([ji1.index, ji2.index]))

        if key in cls.YUKHAP:
            hap_name, element = cls.YUKHAP[key]
            return True, hap_name, element

        return False, "", ""

    @classmethod
    def check_samhap(cls, ji_list: List[JiJi]) -> Tuple[bool, str, str]:
        """삼합 체크 (3개 지지 필요)"""
        if len(ji_list) < 3:
            return False, "", ""

        indices = frozenset([ji.index for ji in ji_list])

        if indices in cls.SAMHAP:
            hap_name, element = cls.SAMHAP[indices]
            return True, hap_name, element

        return False, "", ""

    @classmethod
    def check_banghap(cls, ji_list: List[JiJi]) -> Tuple[bool, str, str]:
        """방합 체크 (3개 지지 필요)"""
        if len(ji_list) < 3:
            return False, "", ""

        indices = frozenset([ji.index for ji in ji_list])

        if indices in cls.BANGHAP:
            hap_name, element = cls.BANGHAP[indices]
            return True, hap_name, element

        return False, "", ""

    @classmethod
    def check_chung(cls, ji1: JiJi, ji2: JiJi) -> bool:
        """육충 체크"""
        key = tuple(sorted([ji1.index, ji2.index]))
        return key in cls.YUKCHUNG

    @classmethod
    def check_hyeong(cls, ji_list: List[JiJi]) -> Tuple[bool, str]:
        """삼형 체크"""
        if len(ji_list) < 2:
            return False, ""

        indices = frozenset([ji.index for ji in ji_list])

        for hyeong_set in cls.SAMHYEONG:
            if indices == hyeong_set:
                if hyeong_set == frozenset([2, 5, 8]):
                    return True, "인사신 무은지형"
                elif hyeong_set == frozenset([1, 4, 7]):
                    return True, "축술미 지세지형"
                elif hyeong_set == frozenset([0, 3]):
                    return True, "자묘 무례지형"

        return False, ""

    @classmethod
    def check_hae(cls, ji1: JiJi, ji2: JiJi) -> bool:
        """육해 체크"""
        key = tuple(sorted([ji1.index, ji2.index]))
        return key in cls.YUKHAE

    @classmethod
    def check_pa(cls, ji1: JiJi, ji2: JiJi) -> bool:
        """육파 체크"""
        key = tuple(sorted([ji1.index, ji2.index]))
        return key in cls.YUKPA


class HyeongchungAnalyzer:
    """형충회합 종합 분석기"""

    @classmethod
    def analyze_saju(
        cls,
        year_gan: CheonGan, year_ji: JiJi,
        month_gan: CheonGan, month_ji: JiJi,
        day_gan: CheonGan, day_ji: JiJi,
        hour_gan: CheonGan, hour_ji: JiJi
    ) -> Dict:
        """
        사주 내 형충회합 분석

        Returns:
            {
                "cheongan_relations": [...],
                "jiji_relations": [...],
                "summary": "..."
            }
        """
        gans = [year_gan, month_gan, day_gan, hour_gan]
        jis = [year_ji, month_ji, day_ji, hour_ji]

        # 천간 관계
        cheongan_relations = cls._analyze_cheongan(gans)

        # 지지 관계
        jiji_relations = cls._analyze_jiji(jis)

        # 요약
        summary = cls._generate_summary(cheongan_relations, jiji_relations)

        return {
            "cheongan_relations": cheongan_relations,
            "jiji_relations": jiji_relations,
            "summary": summary,
            "has_major_conflict": cls._has_major_conflict(cheongan_relations, jiji_relations)
        }

    @classmethod
    def _analyze_cheongan(cls, gans: List[CheonGan]) -> List[Dict]:
        """천간 관계 분석"""
        relations = []

        for i in range(len(gans)):
            for j in range(i + 1, len(gans)):
                gan1, gan2 = gans[i], gans[j]

                # 합 체크
                is_hap, hap_name, element = CheonganRelation.check_hap(gan1, gan2)
                if is_hap:
                    relations.append({
                        "type": "천간합",
                        "position": f"{['년간', '월간', '일간', '시간'][i]}-{['년간', '월간', '일간', '시간'][j]}",
                        "detail": hap_name,
                        "result_element": element,
                        "impact": "길(吉) - 조화와 협력"
                    })

                # 충 체크
                if CheonganRelation.check_chung(gan1, gan2):
                    relations.append({
                        "type": "천간충",
                        "position": f"{['년간', '월간', '일간', '시간'][i]}-{['년간', '월간', '일간', '시간'][j]}",
                        "detail": f"{gan1.korean}{gan2.korean}충",
                        "impact": "흉(凶) - 갈등과 대립"
                    })

        return relations

    @classmethod
    def _analyze_jiji(cls, jis: List[JiJi]) -> List[Dict]:
        """지지 관계 분석"""
        relations = []

        # 육합
        for i in range(len(jis)):
            for j in range(i + 1, len(jis)):
                ji1, ji2 = jis[i], jis[j]

                is_hap, hap_name, element = JijiRelation.check_yukhap(ji1, ji2)
                if is_hap:
                    relations.append({
                        "type": "육합",
                        "position": f"{['년지', '월지', '일지', '시지'][i]}-{['년지', '월지', '일지', '시지'][j]}",
                        "detail": hap_name,
                        "result_element": element,
                        "impact": "길(吉) - 좋은 인연"
                    })

        # 삼합
        is_samhap, samhap_name, samhap_element = JijiRelation.check_samhap(jis)
        if is_samhap:
            relations.append({
                "type": "삼합",
                "position": "년월일시",
                "detail": samhap_name,
                "result_element": samhap_element,
                "impact": "대길(大吉) - 강력한 기운"
            })

        # 방합
        is_banghap, banghap_name, banghap_element = JijiRelation.check_banghap(jis)
        if is_banghap:
            relations.append({
                "type": "방합",
                "position": "년월일시",
                "detail": banghap_name,
                "result_element": banghap_element,
                "impact": "대길(大吉) - 강한 방향성"
            })

        # 육충
        for i in range(len(jis)):
            for j in range(i + 1, len(jis)):
                ji1, ji2 = jis[i], jis[j]

                if JijiRelation.check_chung(ji1, ji2):
                    relations.append({
                        "type": "육충",
                        "position": f"{['년지', '월지', '일지', '시지'][i]}-{['년지', '월지', '일지', '시지'][j]}",
                        "detail": f"{ji1.korean}{ji2.korean}충",
                        "impact": "흉(凶) - 변동과 충돌"
                    })

        # 삼형
        is_hyeong, hyeong_name = JijiRelation.check_hyeong(jis)
        if is_hyeong:
            relations.append({
                "type": "삼형",
                "position": "년월일시",
                "detail": hyeong_name,
                "impact": "흉(凶) - 형벌과 재난"
            })

        # 육해
        for i in range(len(jis)):
            for j in range(i + 1, len(jis)):
                ji1, ji2 = jis[i], jis[j]

                if JijiRelation.check_hae(ji1, ji2):
                    relations.append({
                        "type": "육해",
                        "position": f"{['년지', '월지', '일지', '시지'][i]}-{['년지', '월지', '일지', '시지'][j]}",
                        "detail": f"{ji1.korean}{ji2.korean}해",
                        "impact": "흉(凶) - 손해와 장애"
                    })

        # 육파
        for i in range(len(jis)):
            for j in range(i + 1, len(jis)):
                ji1, ji2 = jis[i], jis[j]

                if JijiRelation.check_pa(ji1, ji2):
                    relations.append({
                        "type": "육파",
                        "position": f"{['년지', '월지', '일지', '시지'][i]}-{['년지', '월지', '일지', '시지'][j]}",
                        "detail": f"{ji1.korean}{ji2.korean}파",
                        "impact": "흉(凶) - 파괴와 손실"
                    })

        return relations

    @classmethod
    def _generate_summary(
        cls,
        cheongan_relations: List[Dict],
        jiji_relations: List[Dict]
    ) -> str:
        """형충회합 요약 생성"""
        summary_parts = []

        # 길한 관계
        good_relations = [r for r in cheongan_relations + jiji_relations if "길" in r["impact"]]
        if good_relations:
            summary_parts.append(f"길한 관계 {len(good_relations)}개")

        # 흉한 관계
        bad_relations = [r for r in cheongan_relations + jiji_relations if "흉" in r["impact"]]
        if bad_relations:
            summary_parts.append(f"흉한 관계 {len(bad_relations)}개")

        if not summary_parts:
            return "특별한 형충회합이 없습니다."

        return ", ".join(summary_parts)

    @classmethod
    def _has_major_conflict(
        cls,
        cheongan_relations: List[Dict],
        jiji_relations: List[Dict]
    ) -> bool:
        """주요 충돌 여부 (일간/일지 관련)"""
        all_relations = cheongan_relations + jiji_relations

        for rel in all_relations:
            if "흉" in rel["impact"] and ("일간" in rel["position"] or "일지" in rel["position"]):
                return True

        return False
