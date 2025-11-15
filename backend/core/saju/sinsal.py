"""
신살(神殺) 분석 모듈

주요 신살:
- 천을귀인(天乙貴人): 가장 좋은 귀인
- 역마살(驛馬殺): 이동과 변화
- 도화살(桃花殺): 이성운, 인기
- 화개살(華蓋殺): 예술, 종교, 고독
- 백호대살(白虎大殺): 재난, 사고
- 양인살(羊刃殺): 날카로움, 위험
- 천라지망(天羅地網): 속박, 제약
"""

from typing import List, Dict, Set
from .gapja import CheonGan, JiJi


class Sinsal:
    """신살 계산 클래스"""

    # 천을귀인 (일간별)
    CHEONUL_GWIIN = {
        0: [1, 7],    # 갑일: 축, 미
        1: [0, 8],    # 을일: 자, 신
        2: [11, 9],   # 병일: 해, 유
        3: [10, 9],   # 정일: 술, 유
        4: [11, 9],   # 무일: 해, 유
        5: [0, 8],    # 기일: 자, 신
        6: [1, 7],    # 경일: 축, 미
        7: [2, 6],    # 신일: 인, 오
        8: [3, 5],    # 임일: 묘, 사
        9: [3, 5],    # 계일: 묘, 사
    }

    # 역마살 (년지/일지 기준)
    YEOKMA_SAL = {
        # 신자진: 인
        frozenset([8, 0, 4]): 2,   # 인
        # 사유축: 해
        frozenset([5, 9, 1]): 11,  # 해
        # 인오술: 신
        frozenset([2, 6, 10]): 8,  # 신
        # 해묘미: 사
        frozenset([11, 3, 7]): 5,  # 사
    }

    # 도화살 (년지/일지 기준)
    DOHWA_SAL = {
        # 신자진: 유
        frozenset([8, 0, 4]): 9,   # 유
        # 사유축: 오
        frozenset([5, 9, 1]): 6,   # 오
        # 인오술: 묘
        frozenset([2, 6, 10]): 3,  # 묘
        # 해묘미: 자
        frozenset([11, 3, 7]): 0,  # 자
    }

    # 화개살 (년지/일지 기준)
    HWAGAE_SAL = {
        # 신자진: 진
        frozenset([8, 0, 4]): 4,   # 진
        # 사유축: 축
        frozenset([5, 9, 1]): 1,   # 축
        # 인오술: 술
        frozenset([2, 6, 10]): 10, # 술
        # 해묘미: 미
        frozenset([11, 3, 7]): 7,  # 미
    }

    # 양인살 (일간별)
    YANGIN_SAL = {
        0: 3,   # 갑일: 묘
        1: 2,   # 을일: 인
        2: 6,   # 병일: 오
        3: 5,   # 정일: 사
        4: 6,   # 무일: 오
        5: 5,   # 기일: 사
        6: 9,   # 경일: 유
        7: 8,   # 신일: 신
        8: 0,   # 임일: 자
        9: 11,  # 계일: 해
    }

    # 백호대살 (년지 기준)
    BAEKHO_DAESAL = {
        0: 10,  # 자년: 술
        1: 7,   # 축년: 미
        2: 4,   # 인년: 진
        3: 1,   # 묘년: 축
        4: 10,  # 진년: 술
        5: 7,   # 사년: 미
        6: 4,   # 오년: 진
        7: 1,   # 미년: 축
        8: 10,  # 신년: 술
        9: 7,   # 유년: 미
        10: 4,  # 술년: 진
        11: 1,  # 해년: 축
    }

    @classmethod
    def find_cheonul_gwiin(
        cls,
        day_gan: CheonGan,
        jis: List[JiJi]
    ) -> List[str]:
        """천을귀인 찾기"""
        gwiin_indices = cls.CHEONUL_GWIIN.get(day_gan.index, [])
        found = []

        positions = ["년지", "월지", "일지", "시지"]
        for i, ji in enumerate(jis):
            if ji.index in gwiin_indices:
                found.append(f"{positions[i]}({ji.korean})")

        return found

    @classmethod
    def find_yeokma_sal(cls, year_ji: JiJi, jis: List[JiJi]) -> List[str]:
        """역마살 찾기"""
        found = []

        # 년지 기준으로 삼합 그룹 찾기
        for group, yeokma_index in cls.YEOKMA_SAL.items():
            if year_ji.index in group:
                positions = ["년지", "월지", "일지", "시지"]
                for i, ji in enumerate(jis):
                    if ji.index == yeokma_index:
                        found.append(f"{positions[i]}({ji.korean})")
                break

        return found

    @classmethod
    def find_dohwa_sal(cls, year_ji: JiJi, jis: List[JiJi]) -> List[str]:
        """도화살 찾기"""
        found = []

        for group, dohwa_index in cls.DOHWA_SAL.items():
            if year_ji.index in group:
                positions = ["년지", "월지", "일지", "시지"]
                for i, ji in enumerate(jis):
                    if ji.index == dohwa_index:
                        found.append(f"{positions[i]}({ji.korean})")
                break

        return found

    @classmethod
    def find_hwagae_sal(cls, year_ji: JiJi, jis: List[JiJi]) -> List[str]:
        """화개살 찾기"""
        found = []

        for group, hwagae_index in cls.HWAGAE_SAL.items():
            if year_ji.index in group:
                positions = ["년지", "월지", "일지", "시지"]
                for i, ji in enumerate(jis):
                    if ji.index == hwagae_index:
                        found.append(f"{positions[i]}({ji.korean})")
                break

        return found

    @classmethod
    def find_yangin_sal(cls, day_gan: CheonGan, jis: List[JiJi]) -> List[str]:
        """양인살 찾기"""
        yangin_index = cls.YANGIN_SAL.get(day_gan.index)
        if yangin_index is None:
            return []

        found = []
        positions = ["년지", "월지", "일지", "시지"]
        for i, ji in enumerate(jis):
            if ji.index == yangin_index:
                found.append(f"{positions[i]}({ji.korean})")

        return found

    @classmethod
    def find_baekho_daesal(cls, year_ji: JiJi, jis: List[JiJi]) -> List[str]:
        """백호대살 찾기"""
        baekho_index = cls.BAEKHO_DAESAL.get(year_ji.index)
        if baekho_index is None:
            return []

        found = []
        positions = ["년지", "월지", "일지", "시지"]
        for i, ji in enumerate(jis):
            if ji.index == baekho_index:
                found.append(f"{positions[i]}({ji.korean})")

        return found

    @classmethod
    def analyze_all_sinsal(
        cls,
        day_gan: CheonGan,
        year_ji: JiJi,
        month_ji: JiJi,
        day_ji: JiJi,
        hour_ji: JiJi
    ) -> Dict:
        """
        모든 신살 분석

        Returns:
            {
                "cheonul_gwiin": [...],
                "yeokma_sal": [...],
                "dohwa_sal": [...],
                ...
            }
        """
        jis = [year_ji, month_ji, day_ji, hour_ji]

        result = {
            "천을귀인": {
                "positions": cls.find_cheonul_gwiin(day_gan, jis),
                "meaning": "귀인의 도움, 위기 시 구원",
                "impact": "대길(大吉)"
            },
            "역마살": {
                "positions": cls.find_yeokma_sal(year_ji, jis),
                "meaning": "이동, 변화, 여행, 활동적",
                "impact": "중립 - 직업에 따라 길흉"
            },
            "도화살": {
                "positions": cls.find_dohwa_sal(year_ji, jis),
                "meaning": "이성운, 인기, 매력, 예술",
                "impact": "반길반흉 - 이성 문제 주의"
            },
            "화개살": {
                "positions": cls.find_hwagae_sal(year_ji, jis),
                "meaning": "예술, 종교, 철학, 고독",
                "impact": "중립 - 영적 재능"
            },
            "양인살": {
                "positions": cls.find_yangin_sal(day_gan, jis),
                "meaning": "날카로움, 위험, 수술, 무기",
                "impact": "흉 - 사고 주의"
            },
            "백호대살": {
                "positions": cls.find_baekho_daesal(year_ji, jis),
                "meaning": "재난, 사고, 혈광",
                "impact": "흉 - 조심 필요"
            }
        }

        # 요약
        good_sinsal = [k for k, v in result.items() if v["positions"] and "길" in v["impact"]]
        bad_sinsal = [k for k, v in result.items() if v["positions"] and "흉" in v["impact"]]

        result["summary"] = {
            "total_sinsal": sum(1 for v in result.values() if isinstance(v, dict) and v.get("positions")),
            "good": good_sinsal,
            "bad": bad_sinsal,
            "description": cls._generate_description(good_sinsal, bad_sinsal)
        }

        return result

    @classmethod
    def _generate_description(cls, good: List[str], bad: List[str]) -> str:
        """신살 종합 설명"""
        parts = []

        if good:
            parts.append(f"길신: {', '.join(good)}")

        if bad:
            parts.append(f"흉신: {', '.join(bad)}")

        if not parts:
            return "특별한 신살이 없습니다."

        return " | ".join(parts)
