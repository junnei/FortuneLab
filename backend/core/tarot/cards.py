"""
타로 카드 정의
22장 메이저 아르카나 (Major Arcana)
"""

from typing import Dict, List
from enum import Enum


class TarotCard:
    """타로 카드 클래스"""

    def __init__(
        self,
        number: int,
        name_en: str,
        name_ko: str,
        keywords_upright: List[str],
        keywords_reversed: List[str],
        meaning_upright: str,
        meaning_reversed: str,
        element: str = None,
        astrology: str = None
    ):
        self.number = number
        self.name_en = name_en
        self.name_ko = name_ko
        self.keywords_upright = keywords_upright
        self.keywords_reversed = keywords_reversed
        self.meaning_upright = meaning_upright
        self.meaning_reversed = meaning_reversed
        self.element = element
        self.astrology = astrology

    def to_dict(self, is_reversed: bool = False) -> Dict:
        """딕셔너리로 변환"""
        return {
            "number": self.number,
            "name_en": self.name_en,
            "name_ko": self.name_ko,
            "keywords": self.keywords_reversed if is_reversed else self.keywords_upright,
            "meaning": self.meaning_reversed if is_reversed else self.meaning_upright,
            "position": "역방향" if is_reversed else "정방향",
            "element": self.element,
            "astrology": self.astrology
        }


class MajorArcana:
    """메이저 아르카나 22장"""

    CARDS = {
        0: TarotCard(
            number=0,
            name_en="The Fool",
            name_ko="광대",
            keywords_upright=["새로운 시작", "순수", "모험", "자유", "무한한 가능성"],
            keywords_reversed=["무모함", "경솔함", "방황", "우유부단"],
            meaning_upright="새로운 여정의 시작을 알립니다. 순수한 마음으로 모험을 떠나세요. 두려움 없이 앞으로 나아가는 것이 중요합니다.",
            meaning_reversed="지나친 낙관주의나 무모한 결정을 경계해야 합니다. 계획 없이 행동하면 위험할 수 있습니다.",
            element="공기",
            astrology="천왕성"
        ),
        1: TarotCard(
            number=1,
            name_en="The Magician",
            name_ko="마법사",
            keywords_upright=["창조", "의지력", "능력", "시작", "잠재력 발현"],
            keywords_reversed=["조작", "속임수", "재능 낭비", "우유부단"],
            meaning_upright="당신은 목표를 이룰 수 있는 모든 도구와 능력을 가지고 있습니다. 의지력을 발휘하여 원하는 것을 창조하세요.",
            meaning_reversed="재능을 잘못된 방향으로 사용하거나, 능력을 제대로 발휘하지 못하고 있을 수 있습니다.",
            element="공기",
            astrology="수성"
        ),
        2: TarotCard(
            number=2,
            name_en="The High Priestess",
            name_ko="여사제",
            keywords_upright=["직관", "신비", "내면의 지혜", "무의식", "영적 통찰"],
            keywords_reversed=["비밀", "억압된 감정", "직관 무시"],
            meaning_upright="내면의 목소리에 귀 기울이세요. 직관과 무의식의 지혜가 답을 알고 있습니다.",
            meaning_reversed="직관을 무시하거나 내면의 목소리를 듣지 못하고 있습니다. 은밀한 정보나 숨겨진 진실이 있을 수 있습니다.",
            element="물",
            astrology="달"
        ),
        3: TarotCard(
            number=3,
            name_en="The Empress",
            name_ko="여제",
            keywords_upright=["풍요", "창조성", "양육", "자연", "아름다움"],
            keywords_reversed=["의존", "질식", "창의력 부족"],
            meaning_upright="풍요와 번영의 시기입니다. 창조적 에너지가 넘치며, 돌봄과 양육의 기운이 강합니다.",
            meaning_reversed="과잉 보호나 의존 관계에 주의하세요. 창조적 에너지가 막혀 있을 수 있습니다.",
            element="땅",
            astrology="금성"
        ),
        4: TarotCard(
            number=4,
            name_en="The Emperor",
            name_ko="황제",
            keywords_upright=["권위", "구조", "리더십", "아버지", "안정"],
            keywords_reversed=["독재", "경직", "권위 남용"],
            meaning_upright="질서와 구조가 필요한 시기입니다. 리더십을 발휘하고 책임감 있게 행동하세요.",
            meaning_reversed="지나친 통제나 권위주의에 빠질 수 있습니다. 융통성이 필요합니다.",
            element="불",
            astrology="양자리"
        ),
        5: TarotCard(
            number=5,
            name_en="The Hierophant",
            name_ko="교황",
            keywords_upright=["전통", "교육", "영적 지도", "관습", "도덕"],
            keywords_reversed=["반항", "비정통", "독단"],
            meaning_upright="전통적 가치와 정통적 방법이 도움이 될 것입니다. 스승이나 멘토의 가르침을 구하세요.",
            meaning_reversed="기존의 틀을 깨고 자신만의 길을 찾고자 합니다. 권위에 반항할 수 있습니다.",
            element="땅",
            astrology="황소자리"
        ),
        6: TarotCard(
            number=6,
            name_en="The Lovers",
            name_ko="연인",
            keywords_upright=["사랑", "조화", "선택", "파트너십", "가치관"],
            keywords_reversed=["불화", "잘못된 선택", "가치관 충돌"],
            meaning_upright="중요한 선택의 순간입니다. 사랑과 조화, 파트너십이 강조됩니다.",
            meaning_reversed="관계의 불균형이나 가치관 충돌이 있을 수 있습니다. 선택을 미루지 마세요.",
            element="공기",
            astrology="쌍둥이자리"
        ),
        7: TarotCard(
            number=7,
            name_en="The Chariot",
            name_ko="전차",
            keywords_upright=["의지", "승리", "통제", "진보", "결단"],
            keywords_reversed=["통제 불능", "방향 상실", "공격성"],
            meaning_upright="강한 의지와 결단력으로 목표를 향해 나아갈 때입니다. 승리가 가까이 있습니다.",
            meaning_reversed="방향을 잃었거나 통제력을 잃을 수 있습니다. 감정을 조절하세요.",
            element="물",
            astrology="게자리"
        ),
        8: TarotCard(
            number=8,
            name_en="Strength",
            name_ko="힘",
            keywords_upright=["용기", "인내", "부드러운 힘", "자제력", "연민"],
            keywords_reversed=["자기 의심", "약함", "자제력 부족"],
            meaning_upright="내면의 힘과 용기로 어려움을 극복할 수 있습니다. 부드러움이 강함을 이깁니다.",
            meaning_reversed="자신감 부족이나 자제력 상실에 주의하세요. 내면의 두려움과 마주하세요.",
            element="불",
            astrology="사자자리"
        ),
        9: TarotCard(
            number=9,
            name_en="The Hermit",
            name_ko="은둔자",
            keywords_upright=["내면 탐구", "고독", "지혜", "영적 깨달음", "성찰"],
            keywords_reversed=["고립", "외로움", "현실 도피"],
            meaning_upright="혼자만의 시간을 가지며 내면을 성찰할 때입니다. 지혜와 깨달음을 얻을 것입니다.",
            meaning_reversed="지나친 고립이나 현실 도피에 빠질 수 있습니다. 균형이 필요합니다.",
            element="땅",
            astrology="처녀자리"
        ),
        10: TarotCard(
            number=10,
            name_en="Wheel of Fortune",
            name_ko="운명의 수레바퀴",
            keywords_upright=["변화", "순환", "행운", "운명", "전환점"],
            keywords_reversed=["불운", "저항", "통제 불가"],
            meaning_upright="큰 변화와 전환점이 다가옵니다. 운명의 흐름을 받아들이고 적응하세요.",
            meaning_reversed="좋지 않은 변화나 불운이 있을 수 있습니다. 변화에 저항하지 마세요.",
            element="불",
            astrology="목성"
        ),
        11: TarotCard(
            number=11,
            name_en="Justice",
            name_ko="정의",
            keywords_upright=["공정", "진실", "법", "균형", "인과응보"],
            keywords_reversed=["불공정", "편견", "책임 회피"],
            meaning_upright="진실과 공정함이 승리합니다. 정직하고 공정한 판단이 필요합니다.",
            meaning_reversed="불공정한 대우나 편견이 있을 수 있습니다. 책임을 회피하지 마세요.",
            element="공기",
            astrology="천칭자리"
        ),
        12: TarotCard(
            number=12,
            name_en="The Hanged Man",
            name_ko="매달린 사람",
            keywords_upright=["희생", "관점 전환", "정지", "내려놓음", "깨달음"],
            keywords_reversed=["지연", "저항", "헛된 희생"],
            meaning_upright="잠시 멈추고 새로운 관점에서 바라보세요. 내려놓음을 통해 깨달음을 얻습니다.",
            meaning_reversed="불필요한 희생이나 지연에 빠져 있습니다. 변화에 저항하지 마세요.",
            element="물",
            astrology="해왕성"
        ),
        13: TarotCard(
            number=13,
            name_en="Death",
            name_ko="죽음",
            keywords_upright=["변환", "끝과 시작", "재탄생", "해방", "변화"],
            keywords_reversed=["정체", "변화 거부", "집착"],
            meaning_upright="낡은 것이 끝나고 새로운 것이 시작됩니다. 변화를 두려워하지 마세요.",
            meaning_reversed="변화를 거부하거나 과거에 집착하고 있습니다. 놓아주세요.",
            element="물",
            astrology="전갈자리"
        ),
        14: TarotCard(
            number=14,
            name_en="Temperance",
            name_ko="절제",
            keywords_upright=["균형", "조화", "인내", "중용", "치유"],
            keywords_reversed=["불균형", "과잉", "조급함"],
            meaning_upright="균형과 조화가 필요합니다. 인내심을 가지고 중도를 지키세요.",
            meaning_reversed="균형을 잃었거나 과잉 상태입니다. 절제와 조절이 필요합니다.",
            element="불",
            astrology="궁수자리"
        ),
        15: TarotCard(
            number=15,
            name_en="The Devil",
            name_ko="악마",
            keywords_upright=["속박", "중독", "유혹", "물질주의", "그림자"],
            keywords_reversed=["해방", "깨달음", "탈출"],
            meaning_upright="무언가에 속박되어 있습니다. 집착이나 중독에서 벗어나세요.",
            meaning_reversed="속박에서 벗어나고 있습니다. 스스로를 해방시킬 힘이 있습니다.",
            element="땅",
            astrology="염소자리"
        ),
        16: TarotCard(
            number=16,
            name_en="The Tower",
            name_ko="탑",
            keywords_upright=["파괴", "급격한 변화", "계시", "해체", "깨달음"],
            keywords_reversed=["재난 회피", "두려움", "저항"],
            meaning_upright="갑작스런 변화와 파괴가 올 수 있습니다. 허상이 무너지고 진실이 드러납니다.",
            meaning_reversed="변화를 피하려 하거나 두려워하고 있습니다. 무너질 것은 무너져야 합니다.",
            element="불",
            astrology="화성"
        ),
        17: TarotCard(
            number=17,
            name_en="The Star",
            name_ko="별",
            keywords_upright=["희망", "영감", "평온", "치유", "낙관"],
            keywords_reversed=["절망", "불신", "희망 상실"],
            meaning_upright="희망과 치유의 시기입니다. 미래에 대한 믿음을 가지세요.",
            meaning_reversed="희망을 잃었거나 방향을 상실했습니다. 다시 희망을 찾으세요.",
            element="공기",
            astrology="물병자리"
        ),
        18: TarotCard(
            number=18,
            name_en="The Moon",
            name_ko="달",
            keywords_upright=["환상", "불안", "무의식", "직관", "미지"],
            keywords_reversed=["혼란 해소", "진실 발견", "두려움 극복"],
            meaning_upright="불확실성과 환상이 있습니다. 직관을 믿되 환상에 속지 마세요.",
            meaning_reversed="혼란이 걷히고 진실이 밝혀집니다. 두려움에서 벗어나고 있습니다.",
            element="물",
            astrology="물고기자리"
        ),
        19: TarotCard(
            number=19,
            name_en="The Sun",
            name_ko="태양",
            keywords_upright=["성공", "기쁨", "긍정", "활력", "명료함"],
            keywords_reversed=["과신", "우울", "실패"],
            meaning_upright="성공과 기쁨의 시기입니다. 모든 것이 밝고 명확해집니다.",
            meaning_reversed="일시적 어려움이나 우울이 있을 수 있습니다. 과신을 조심하세요.",
            element="불",
            astrology="태양"
        ),
        20: TarotCard(
            number=20,
            name_en="Judgement",
            name_ko="심판",
            keywords_upright=["부활", "깨달음", "소명", "용서", "재생"],
            keywords_reversed=["자기 비판", "의심", "과거 집착"],
            meaning_upright="새로운 각성과 깨달음의 순간입니다. 과거를 정리하고 새롭게 태어나세요.",
            meaning_reversed="과거에 얽매이거나 자기 비판에 빠져 있습니다. 용서하고 앞으로 나아가세요.",
            element="불",
            astrology="명왕성"
        ),
        21: TarotCard(
            number=21,
            name_en="The World",
            name_ko="세계",
            keywords_upright=["완성", "성취", "여행", "통합", "성공"],
            keywords_reversed=["미완성", "지연", "부족함"],
            meaning_upright="목표 달성과 완성의 시기입니다. 한 사이클이 완성되고 새로운 시작을 준비합니다.",
            meaning_reversed="아직 완성되지 않았거나 무언가 부족합니다. 마지막 노력이 필요합니다.",
            element="땅",
            astrology="토성"
        ),
    }

    @classmethod
    def get_card(cls, number: int) -> TarotCard:
        """카드 번호로 타로 카드 반환"""
        return cls.CARDS.get(number)

    @classmethod
    def get_all_cards(cls) -> List[TarotCard]:
        """모든 메이저 아르카나 카드 반환"""
        return [cls.CARDS[i] for i in range(22)]

    @classmethod
    def get_card_by_name(cls, name: str) -> TarotCard:
        """카드 이름으로 검색"""
        for card in cls.CARDS.values():
            if card.name_en.lower() == name.lower() or card.name_ko == name:
                return card
        return None
