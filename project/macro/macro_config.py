from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SEOUL_TZ = ZoneInfo("Asia/Seoul")


@dataclass(slots=True)
class TicketingConfig:
    # ── 계정 정보 ──────────────────────────────────────────────
    user_id: str = ""          # YES24 아이디
    user_pw: str = ""          # YES24 비밀번호

    # ── 이벤트 정보 ────────────────────────────────────────────
    event_url: str = ""

    # ── 좌석 / 구역 설정 ───────────────────────────────────────
    # 예매 페이지 좌석 구역 XPath (개발자 도구로 확인 후 수정)
    area_xpath: str = '//*[@id="area5"]'
    # 날짜 선택 버튼 CLASS NAME (보통 'select')
    date_select_class: str = "select"

    # ── 결제 설정 ──────────────────────────────────────────────
    # 결제 수단: 무통장 입금 radio XPath
    payment_xpath: str = '//*[@id="rdoPays22"]'
    # 은행 드롭다운에서 선택할 index (0=선택, 1=첫 번째 은행 등)
    bank_select_index: int = 1

    # ── 오픈 카운트다운 설정 ────────────────────────────────────
    open_time: datetime = field(
        default_factory=lambda: datetime.now(SEOUL_TZ).replace(second=0, microsecond=0)
    )
    # 오픈 N초 전부터 브라우저 반복 새로고침 시작
    refresh_seconds_before_open: int = 5
    countdown_interval: float = 0.5

    # ── 기타 ───────────────────────────────────────────────────
    # True 이면 실제 결제 버튼을 누르지 않음 (테스트용)
    dry_run: bool = True
    implicitly_wait: int = 3
    practice_html: Path = field(
        default_factory=lambda: Path(__file__).with_name("ticketing_practice.html")
    )


# ──────────────────────────────────────────────
#  여기에서 자신의 정보를 입력하세요
# ──────────────────────────────────────────────
DEFAULT_CONFIG = TicketingConfig(
    user_id="",       # ← YES24 아이디
    user_pw="",       # ← YES24 비밀번호
    event_url="",  # ← 이벤트 ID 변경
    dry_run=True,                   # ← 실제 결제 시 False 로 변경
)
