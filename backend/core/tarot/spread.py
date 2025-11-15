"""
타로 스프레드 시스템
다양한 타로 카드 배치 방법
"""

from typing import List, Dict
from .cards import TarotCard, MajorArcana
import random


class TarotSpread:
    """타로 스프레드 기본 클래스"""

    def __init__(self, spread_type: str):
        self.spread_type = spread_type
        self.positions = []

    def draw_cards(self, num_cards: int, allow_reversed: bool = True) -> List[Dict]:
        """
        카드 뽑기

        Args:
            num_cards: 뽑을 카드 수
            allow_reversed: 역방향 허용 여부

        Returns:
            뽑힌 카드 리스트 (with position and reversed info)
        """
        # 22장 메이저 아르카나에서 랜덤 선택
        available_numbers = list(range(22))
        selected_numbers = random.sample(available_numbers, num_cards)

        drawn_cards = []
        for i, card_num in enumerate(selected_numbers):
            card = MajorArcana.get_card(card_num)
            is_reversed = random.choice([True, False]) if allow_reversed else False

            drawn_cards.append({
                "position": self.positions[i] if i < len(self.positions) else f"위치{i+1}",
                "card": card.to_dict(is_reversed),
                "is_reversed": is_reversed
            })

        return drawn_cards


class ThreeCardSpread(TarotSpread):
    """3장 스프레드 - 과거/현재/미래"""

    def __init__(self):
        super().__init__("3장 스프레드")
        self.positions = ["과거", "현재", "미래"]

    def draw(self, allow_reversed: bool = True) -> Dict:
        """3장 뽑기"""
        cards = self.draw_cards(3, allow_reversed)

        return {
            "spread_type": self.spread_type,
            "description": "과거-현재-미래의 흐름을 보는 기본 스프레드",
            "cards": {
                "past": cards[0],
                "present": cards[1],
                "future": cards[2]
            }
        }


class CelticCrossSpread(TarotSpread):
    """켈틱 크로스 스프레드 - 10장"""

    def __init__(self):
        super().__init__("켈틱 크로스")
        self.positions = [
            "현재 상황",
            "장애물/도전",
            "과거의 영향",
            "가까운 미래",
            "최선의 결과",
            "가까운 과거",
            "당신의 태도",
            "주변 환경",
            "희망과 두려움",
            "최종 결과"
        ]

    def draw(self, allow_reversed: bool = True) -> Dict:
        """10장 뽑기"""
        cards = self.draw_cards(10, allow_reversed)

        return {
            "spread_type": self.spread_type,
            "description": "가장 포괄적인 타로 스프레드",
            "cards": {
                "present": cards[0],
                "challenge": cards[1],
                "past": cards[2],
                "near_future": cards[3],
                "best_outcome": cards[4],
                "recent_past": cards[5],
                "your_attitude": cards[6],
                "environment": cards[7],
                "hopes_fears": cards[8],
                "final_outcome": cards[9]
            }
        }


class RelationshipSpread(TarotSpread):
    """관계 스프레드 - 5장"""

    def __init__(self):
        super().__init__("관계 스프레드")
        self.positions = [
            "나의 마음",
            "상대방의 마음",
            "현재 관계",
            "장애물",
            "관계의 미래"
        ]

    def draw(self, allow_reversed: bool = True) -> Dict:
        """5장 뽑기"""
        cards = self.draw_cards(5, allow_reversed)

        return {
            "spread_type": self.spread_type,
            "description": "두 사람의 관계를 분석하는 스프레드",
            "cards": {
                "your_feelings": cards[0],
                "their_feelings": cards[1],
                "current_relationship": cards[2],
                "obstacles": cards[3],
                "future": cards[4]
            }
        }


class YesNoSpread(TarotSpread):
    """예/아니오 스프레드 - 1장"""

    def __init__(self):
        super().__init__("Yes/No 스프레드")
        self.positions = ["답"]

    def draw(self, allow_reversed: bool = False) -> Dict:
        """1장 뽑기"""
        cards = self.draw_cards(1, allow_reversed)
        card_data = cards[0]["card"]

        # 정방향 긍정 카드들
        positive_cards = [
            "The Sun", "The World", "The Star", "The Magician",
            "The Empress", "The Emperor", "Strength", "The Chariot"
        ]

        is_yes = card_data["name_en"] in positive_cards

        return {
            "spread_type": self.spread_type,
            "description": "간단한 예/아니오 질문에 대한 답",
            "cards": {
                "answer": cards[0]
            },
            "result": "예(Yes)" if is_yes else "아니오(No)",
            "confidence": "높음" if card_data["name_en"] in ["The Sun", "The World", "The Tower", "Death"] else "중간"
        }


def get_spread(spread_type: str) -> TarotSpread:
    """스프레드 타입으로 스프레드 객체 반환"""
    spreads = {
        "three_card": ThreeCardSpread,
        "celtic_cross": CelticCrossSpread,
        "relationship": RelationshipSpread,
        "yes_no": YesNoSpread
    }

    spread_class = spreads.get(spread_type, ThreeCardSpread)
    return spread_class()
