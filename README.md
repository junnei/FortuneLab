# 🔮 FortuneLab

**AI 기반 사주/타로 웹서비스**

생년월일시와 출생지를 입력하면 정확한 만세력 계산과 자평명리학 기반 AI 해석을 제공합니다.
타로 카드로 현재와 미래를 탐색하고, AI 타로리스트와 대화할 수 있습니다.

## 🌟 주요 기능

### 📅 사주 만세력 (결정론적 계산)
- **정확한 사주팔자 계산**
  - 생년월일시 + 출생지 경도 보정
  - 24절기 기준 월주 계산
  - 음력/양력 변환 지원
  - 진태양시 계산

- **대운(大運) / 세운(歲運)**
  - 10년 주기 대운 계산
  - 현재 나이 기준 대운 확인
  - 년운/월운 분석

- **형충회합(刑沖會合)**
  - 천간오합, 지지육합
  - 삼합, 방합
  - 육충, 삼형, 육해, 육파

- **십이운성(十二運星)**
  - 장생, 목욕, 관대, 건록, 제왕...
  - 일간 기준 생로병사 분석

- **신살(神殺)**
  - 천을귀인, 역마살, 도화살
  - 화개살, 양인살, 백호대살

- **AI 해석 (자평명리학)**
  - 적천수, 연해자평 기반
  - 격국론, 용신론
  - 성격, 재물운, 직업운 해석

### 🎴 타로
- **다양한 스프레드**
  - 3장 스프레드 (과거/현재/미래)
  - 켈틱 크로스 (10장)
  - 관계 스프레드 (5장)
  - Yes/No 스프레드 (1장)

- **22 메이저 아르카나**
  - 정방향/역방향 해석
  - 상징과 의미
  - 원소와 점성술 대응

- **AI 타로 리딩**
  - 전문 타로리스트 수준 해석
  - 직관적이고 공감적인 메시지
  - 실용적 조언

### 💬 대화형 상담
- 사주/타로 결과 기반 채팅
- 추가 질문 및 심화 상담

## 🏗️ 아키텍처

```
┌─────────────────┐
│   Frontend      │  Next.js 14 (Vercel)
│   (Vercel)      │  - React
└────────┬────────┘  - TypeScript
         │           - Tailwind CSS
         │ REST API
         ↓
┌─────────────────┐
│   Backend       │  FastAPI (Railway)
│   (Railway)     │  - Python 3.11
└────────┬────────┘  - LangChain/LangGraph
         │           - OpenAI/Anthropic
         │
    ┌────┴─────┬──────────────┬───────────────┐
    │          │              │               │
┌───┴───┐  ┌──┴──┐     ┌────┴─────┐   ┌────┴──────┐
│ 만세력  │  │ 타로 │     │ 사주 Agent │   │ 타로 Agent │
│ 계산   │  │ 카드 │     │           │   │           │
└───────┘  └─────┘     └──────────┘   └───────────┘
```

## 📂 프로젝트 구조

```
FortuneLab/
├── backend/                    # FastAPI 백엔드
│   ├── core/                   # 핵심 로직 (결정론적)
│   │   ├── saju/              # 사주 계산
│   │   │   ├── gapja.py       # 60갑자
│   │   │   ├── solar_terms.py # 24절기
│   │   │   ├── location.py    # 경도 보정
│   │   │   ├── calculator.py  # 사주팔자
│   │   │   ├── daeun.py       # 대운/세운
│   │   │   ├── hyeongchung.py # 형충회합
│   │   │   ├── sibiunseong.py # 십이운성
│   │   │   ├── sinsal.py      # 신살
│   │   │   └── manseryeok.py  # 만세력 통합
│   │   └── tarot/             # 타로
│   │       ├── cards.py       # 22 메이저 아르카나
│   │       └── spread.py      # 스프레드
│   ├── agents/                # AI 에이전트
│   │   ├── saju_agent.py      # 사주 해석
│   │   └── tarot_agent.py     # 타로 해석
│   ├── api/                   # API 라우트
│   │   └── routes.py
│   ├── models/                # Pydantic 스키마
│   │   └── schemas.py
│   ├── main.py                # FastAPI 앱
│   ├── Dockerfile             # Railway 배포
│   ├── railway.json
│   └── requirements.txt
│
└── frontend/                  # Next.js 프론트엔드 (예정)
    └── ...
```

## 🚀 빠른 시작

### 백엔드 로컬 실행

1. **환경 설정**
```bash
cd backend
cp .env.example .env
# .env 파일에 API 키 입력
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **서버 실행**
```bash
uvicorn backend.main:app --reload
```

4. **API 테스트**
- http://localhost:8000/api/health
- http://localhost:8000/docs (Swagger UI)

### Railway 배포

1. **Railway 프로젝트 생성**
```bash
railway login
railway init
```

2. **환경 변수 설정**
```bash
railway variables set OPENAI_API_KEY=your_key
railway variables set ANTHROPIC_API_KEY=your_key
```

3. **배포**
```bash
railway up
```

## 📡 API 엔드포인트

### 사주

**POST `/api/saju/calculate`**
- 만세력 계산 (결정론적)
- 입력: 생년월일시, 성별, 출생지
- 출력: 사주팔자, 대운, 세운, 형충회합, 십이운성, 신살

**POST `/api/saju/interpret`**
- AI 해석
- 입력: 만세력 결과, 질문
- 출력: 자평명리학 기반 해석

### 타로

**POST `/api/tarot/draw`**
- 타로 카드 뽑기
- 입력: 스프레드 타입, 질문
- 출력: 뽑힌 카드

**POST `/api/tarot/interpret`**
- AI 해석
- 입력: 카드 결과, 질문, 상황
- 출력: 타로 리딩

### 채팅

**POST `/api/chat`**
- 대화형 상담
- 입력: 서비스 타입, 세션 데이터, 메시지
- 출력: AI 응답

## 🔑 환경 변수

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Frontend URL (CORS)
FRONTEND_URL=https://your-frontend.vercel.app

# Environment
ENV=production
```

## 🛠️ 기술 스택

### Backend
- **Python 3.11**
- **FastAPI** - 고성능 REST API
- **LangChain** - AI 에이전트 프레임워크
- **korean-lunar-calendar** - 음력 변환
- **geopy** - 지리 정보
- **OpenAI / Anthropic** - LLM

### Frontend (예정)
- **Next.js 14** - React 프레임워크
- **TypeScript** - 타입 안전성
- **Tailwind CSS** - 스타일링
- **React Query** - 상태 관리

### Deployment
- **Railway** - 백엔드 호스팅
- **Vercel** - 프론트엔드 호스팅

## 📚 참고 문헌

### 자평명리학
- 서낙오(徐樂吾) - 적천수천미(滴天髓闡微)
- 만육오(萬育吾) - 삼명통회(三命通會)
- 유백온(劉伯溫) - 적천수(滴天髓)

### 타로
- Rider-Waite Tarot Deck
- The Pictorial Key to the Tarot - A. E. Waite
- Jung's Archetypes

## 📄 라이센스

MIT License

## 👥 기여

이슈 및 PR 환영합니다!

## 🔮 향후 계획

- [ ] 프론트엔드 UI/UX 구현
- [ ] LangGraph 멀티 에이전트 슈퍼바이저
- [ ] WebSocket 실시간 채팅
- [ ] 궁합 분석 기능
- [ ] 사주 PDF 다운로드
- [ ] 타로 저널 기능
- [ ] 소셜 로그인
- [ ] 결제 시스템

---

Made with ❤️ by FortuneLab Team
