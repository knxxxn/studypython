"""
안드로이드 탭 매크로 실행기.

이 파일은 폰이나 태블릿에서 직접 실행해서 사용할 수 있게 만든 버전입니다.
PC에서 쓰는 기존 마우스 매크로와 달리, 안드로이드 셸의 `input tap` 명령을 이용해
지정한 시간에 화면을 탭합니다.

사용 예시:

1. 폰에서 실행 후 질문에 따라 직접 입력할 때
   python click_android.py

2. 안드로이드 셸에서 `input tap` 명령을 직접 실행할 수 있을 때
   python click_android.py --x 540 --y 1200 --at "2026-03-30 20:00:00.000"

3. 다른 PC에서 ADB를 통해 기기에 명령을 보낼 때
   python click_android.py --x 540 --y 1200 --after 5 --shell-prefix "adb shell input"

주의:
- 일반적인 안드로이드 앱은 다른 앱 화면에 마음대로 탭을 넣지 못합니다.
- 이 스크립트는 `adb shell`, 루트 권한, 또는 비슷한 수준의 셸 권한이 있어야
  실제 탭 명령을 보낼 수 있습니다.
- 좌표는 직접 입력해야 합니다.
- 좌표 확인은 `adb shell wm size` 또는 안드로이드 개발자 옵션의
  포인터 위치 표시 기능을 활용하면 됩니다.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import time
from datetime import datetime, timedelta


DEFAULT_POLL_INTERVAL = 0.05


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="안드로이드 화면 탭을 셸 명령으로 예약 실행합니다."
    )
    parser.add_argument("--x", type=int, help="탭할 X 좌표")
    parser.add_argument("--y", type=int, help="탭할 Y 좌표")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="탭할 횟수",
    )
    parser.add_argument(
        "--delay-ms",
        type=int,
        default=100,
        help="탭 사이의 대기 시간(밀리초)",
    )
    parser.add_argument(
        "--at",
        help='실행 시각. 형식: "YYYY-MM-DD HH:MM:SS" 또는 "YYYY-MM-DD HH:MM:SS.mmm"',
    )
    parser.add_argument(
        "--after",
        type=float,
        help="현재 시각 기준 N초 뒤에 실행",
    )
    parser.add_argument(
        "--shell-prefix",
        default="input",
        help='탭 명령을 보낼 셸 접두어. 예: "input" 또는 "adb shell input"',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실행하지 않고 명령어만 출력",
    )
    return parser.parse_args(argv)


def parse_target_time(value: str) -> datetime:
    formats = (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError("지원하지 않는 시간 형식입니다")


def resolve_target(args: argparse.Namespace) -> datetime:
    if bool(args.at) == bool(args.after is not None):
        raise ValueError("--at 또는 --after 중 하나만 사용해야 합니다")

    if args.at:
        target = parse_target_time(args.at)
    else:
        target = datetime.now() + timedelta(seconds=args.after)

    if target <= datetime.now():
        raise ValueError("실행 시각은 현재보다 미래여야 합니다")

    return target


def validate_args(args: argparse.Namespace) -> None:
    if args.x is None or args.y is None:
        raise ValueError("X 좌표와 Y 좌표를 입력해야 합니다")
    if args.count < 1:
        raise ValueError("--count는 1 이상이어야 합니다")
    if args.delay_ms < 0:
        raise ValueError("--delay-ms는 0 이상이어야 합니다")


def prompt_text(message: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{message}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("값을 입력해주세요.")


def prompt_int(message: str, default: int | None = None, minimum: int | None = None) -> int:
    while True:
        raw = prompt_text(message, None if default is None else str(default))
        try:
            value = int(raw)
        except ValueError:
            print("숫자로 입력해주세요.")
            continue
        if minimum is not None and value < minimum:
            print(f"{minimum} 이상으로 입력해주세요.")
            continue
        return value


def prompt_float(
    message: str,
    default: float | None = None,
    minimum: float | None = None,
) -> float:
    while True:
        raw = prompt_text(message, None if default is None else str(default))
        try:
            value = float(raw)
        except ValueError:
            print("숫자로 입력해주세요.")
            continue
        if minimum is not None and value < minimum:
            print(f"{minimum} 이상으로 입력해주세요.")
            continue
        return value


def prompt_target_mode() -> tuple[str | None, float | None]:
    print("실행 방식을 선택하세요.")
    print("1. 특정 시각에 실행")
    print("2. 몇 초 뒤에 실행")

    while True:
        choice = prompt_text("번호 입력", "2")
        if choice == "1":
            at_value = prompt_text(
                "실행 시각 입력",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            return at_value, None
        if choice == "2":
            after_value = prompt_float("몇 초 뒤에 실행할까요?", 5, 0)
            return None, after_value
        print("1 또는 2만 입력해주세요.")


def prompt_args() -> argparse.Namespace:
    print("안드로이드 탭 매크로 설정을 시작합니다.")
    print("좌표는 직접 입력해야 하며, 실제 탭 실행은 안드로이드 셸 권한이 필요합니다.")
    print()

    x = prompt_int("X 좌표", minimum=0)
    y = prompt_int("Y 좌표", minimum=0)
    count = prompt_int("탭 횟수", default=1, minimum=1)
    delay_ms = prompt_int("탭 간격(ms)", default=100, minimum=0)
    at_value, after_value = prompt_target_mode()
    shell_prefix = prompt_text("셸 명령 접두어", "input")
    dry_run_answer = prompt_text("테스트 모드로 실행할까요? (y/n)", "n").lower()
    dry_run = dry_run_answer in {"y", "yes", "ㅛ"}

    return argparse.Namespace(
        x=x,
        y=y,
        count=count,
        delay_ms=delay_ms,
        at=at_value,
        after=after_value,
        shell_prefix=shell_prefix,
        dry_run=dry_run,
    )


def build_tap_command(shell_prefix: str, x: int, y: int) -> list[str]:
    prefix_parts = shlex.split(shell_prefix)
    return prefix_parts + ["tap", str(x), str(y)]


def wait_until(target: datetime) -> None:
    while True:
        remaining = (target - datetime.now()).total_seconds()
        if remaining <= 0:
            return
        if remaining > 0.5:
            time.sleep(min(remaining / 2, 0.2))
        else:
            time.sleep(DEFAULT_POLL_INTERVAL)


def run_taps(command: list[str], count: int, delay_ms: int, dry_run: bool) -> None:
    for index in range(count):
        if dry_run:
            print("[테스트 모드]", " ".join(command))
        else:
            subprocess.run(command, check=True)

        if index < count - 1 and delay_ms > 0:
            time.sleep(delay_ms / 1000)


def main() -> int:
    if len(sys.argv) == 1:
        args = prompt_args()
    else:
        args = parse_args()

    try:
        validate_args(args)
        target = resolve_target(args)
    except ValueError as exc:
        print(f"인자 오류: {exc}")
        return 2

    command = build_tap_command(args.shell_prefix, args.x, args.y)

    print(f"대기 중: {target.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
    print(f"탭 좌표: ({args.x}, {args.y}), 횟수={args.count}, 간격={args.delay_ms}ms")
    print("실행 명령:", " ".join(command))

    try:
        wait_until(target)
        run_taps(command, args.count, args.delay_ms, args.dry_run)
    except FileNotFoundError:
        print("셸 명령을 찾지 못했습니다. --shell-prefix, ADB 연결, 안드로이드 셸 권한을 확인하세요.")
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"탭 명령 실행 실패: 종료 코드 {exc.returncode}")
        return exc.returncode
    except KeyboardInterrupt:
        print("사용자에 의해 취소되었습니다")
        return 130

    print("완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
