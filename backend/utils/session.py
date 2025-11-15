"""
통합 세션 관리 시스템
사주와 타로 결과를 하나의 세션에 저장하여 서로 참조 가능
"""

from typing import Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel
import uuid


class SessionData(BaseModel):
    """세션 데이터"""
    session_id: str
    created_at: str
    saju_result: Optional[Dict] = None
    tarot_result: Optional[Dict] = None
    conversation_history: List[Dict] = []
    user_info: Optional[Dict] = None  # 추가 사용자 정보


class SessionManager:
    """세션 관리자 (인메모리 저장소)"""

    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}

    def create_session(self, user_info: Optional[Dict] = None) -> str:
        """
        새 세션 생성

        Returns:
            session_id
        """
        session_id = str(uuid.uuid4())

        session = SessionData(
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            user_info=user_info
        )

        self._sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """세션 조회"""
        return self._sessions.get(session_id)

    def update_saju(self, session_id: str, saju_result: Dict) -> bool:
        """세션에 사주 결과 저장"""
        session = self.get_session(session_id)
        if session:
            session.saju_result = saju_result
            return True
        return False

    def update_tarot(self, session_id: str, tarot_result: Dict) -> bool:
        """세션에 타로 결과 저장"""
        session = self.get_session(session_id)
        if session:
            session.tarot_result = tarot_result
            return True
        return False

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        service_type: str = "general"
    ) -> bool:
        """대화 메시지 추가"""
        session = self.get_session(session_id)
        if session:
            session.conversation_history.append({
                "role": role,
                "content": content,
                "service_type": service_type,
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

    def get_conversation_history(
        self,
        session_id: str,
        service_type: Optional[str] = None
    ) -> List[Dict]:
        """
        대화 히스토리 조회

        Args:
            session_id: 세션 ID
            service_type: 특정 서비스 타입만 필터링 (None이면 전체)

        Returns:
            대화 메시지 리스트
        """
        session = self.get_session(session_id)
        if not session:
            return []

        if service_type:
            return [
                msg for msg in session.conversation_history
                if msg.get("service_type") == service_type
            ]

        return session.conversation_history

    def has_saju(self, session_id: str) -> bool:
        """사주 결과가 있는지 확인"""
        session = self.get_session(session_id)
        return session and session.saju_result is not None

    def has_tarot(self, session_id: str) -> bool:
        """타로 결과가 있는지 확인"""
        session = self.get_session(session_id)
        return session and session.tarot_result is not None

    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """세션 요약 정보"""
        session = self.get_session(session_id)
        if not session:
            return None

        return {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "has_saju": session.saju_result is not None,
            "has_tarot": session.tarot_result is not None,
            "message_count": len(session.conversation_history),
            "user_info": session.user_info
        }

    def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup_old_sessions(self, hours: int = 24):
        """오래된 세션 정리 (24시간 이상 지난 것)"""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        to_delete = []

        for session_id, session in self._sessions.items():
            created = datetime.fromisoformat(session.created_at)
            if created < cutoff:
                to_delete.append(session_id)

        for session_id in to_delete:
            self.delete_session(session_id)

        return len(to_delete)


# 전역 세션 매니저 (싱글톤)
_session_manager = None


def get_session_manager() -> SessionManager:
    """세션 매니저 싱글톤 인스턴스"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
