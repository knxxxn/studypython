"""
사용법
좌표 알아내기 - "좌표 입력" 버튼 클릭 → 3초 카운트다운 동안 클릭할 위치에 마우스를 올려놓기 → 자동으로 X, Y 좌표가 입력됨
시간 설정 - 클릭할 시간을 년/월/일/시/분/초/밀리초까지 설정
딜레이/횟수 - 여러 번 클릭할 경우 횟수와 클릭 간격(ms) 설정
"설정" 버튼 클릭 → 해당 시간이 되면 자동 클릭 실행

예를 들어 Fans 이벤트 신청 버튼이 20시에 열린다면:
미리 버튼 위치에 마우스 올려놓고 "좌표 입력"
시간을 20시 00분 00초 0으로 설정
"설정" 누르고 대기
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
import pyautogui

pyautogui.FAILSAFE = False


class ClickMacro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("클릭 매크로")
        self.root.resizable(False, False)
        self.timer_active = False

        self._build_ui()

    def _build_ui(self):
        # ── 시간 설정 ──
        time_frame = tk.LabelFrame(self.root, text="시간", padx=10, pady=5)
        time_frame.pack(padx=10, pady=5, fill="x")

        row1 = tk.Frame(time_frame)
        row1.pack(pady=2)

        now = datetime.now()
        self.year = tk.Spinbox(row1, from_=2024, to=2030, width=5, format="%04.0f")
        self.year.delete(0, "end")
        self.year.insert(0, f"{now.year}")
        self.year.pack(side="left")
        tk.Label(row1, text="년").pack(side="left")

        self.month = tk.Spinbox(row1, from_=1, to=12, width=3, format="%02.0f")
        self.month.delete(0, "end")
        self.month.insert(0, f"{now.month}")
        self.month.pack(side="left")
        tk.Label(row1, text="월").pack(side="left")

        self.day = tk.Spinbox(row1, from_=1, to=31, width=3, format="%02.0f")
        self.day.delete(0, "end")
        self.day.insert(0, f"{now.day}")
        self.day.pack(side="left")
        tk.Label(row1, text="일").pack(side="left")

        row2 = tk.Frame(time_frame)
        row2.pack(pady=2)

        self.hour = tk.Spinbox(row2, from_=0, to=23, width=3, format="%02.0f")
        self.hour.delete(0, "end")
        self.hour.insert(0, f"{now.hour}")
        self.hour.pack(side="left")
        tk.Label(row2, text="시").pack(side="left")

        self.minute = tk.Spinbox(row2, from_=0, to=59, width=3, format="%02.0f")
        self.minute.delete(0, "end")
        self.minute.insert(0, f"{now.minute}")
        self.minute.pack(side="left")
        tk.Label(row2, text="분").pack(side="left")

        self.second = tk.Spinbox(row2, from_=0, to=59, width=3, format="%02.0f")
        self.second.delete(0, "end")
        self.second.insert(0, f"{now.second}")
        self.second.pack(side="left")
        tk.Label(row2, text="초").pack(side="left")

        self.ms = tk.Spinbox(row2, from_=0, to=999, width=4)
        self.ms.delete(0, "end")
        self.ms.insert(0, "0")
        self.ms.pack(side="left")

        # ── 좌표 설정 ──
        coord_frame = tk.LabelFrame(self.root, text="좌표", padx=10, pady=5)
        coord_frame.pack(padx=10, pady=5, fill="x")

        coord_row1 = tk.Frame(coord_frame)
        coord_row1.pack(pady=2)
        tk.Label(coord_row1, text="X", width=5).pack(side="left")
        self.x_entry = tk.Entry(coord_row1, width=8)
        self.x_entry.pack(side="left")

        coord_row2 = tk.Frame(coord_frame)
        coord_row2.pack(pady=2)
        tk.Label(coord_row2, text="Y", width=5).pack(side="left")
        self.y_entry = tk.Entry(coord_row2, width=8)
        self.y_entry.pack(side="left")

        self.capture_btn = tk.Button(
            coord_frame, text="좌표 입력", command=self._capture_position
        )
        self.capture_btn.pack(side="right", padx=5)

        # 딜레이
        delay_row = tk.Frame(coord_frame)
        delay_row.pack(pady=2)
        tk.Label(delay_row, text="딜레이", width=5).pack(side="left")
        self.delay_entry = tk.Entry(delay_row, width=8)
        self.delay_entry.insert(0, "100")
        self.delay_entry.pack(side="left")
        tk.Label(delay_row, text="ms").pack(side="left")

        # 클릭 횟수
        count_row = tk.Frame(coord_frame)
        count_row.pack(pady=2)
        tk.Label(count_row, text="횟수", width=5).pack(side="left")
        self.count_entry = tk.Entry(count_row, width=8)
        self.count_entry.insert(0, "1")
        self.count_entry.pack(side="left")
        tk.Label(count_row, text="회").pack(side="left")

        # ── 버튼 ──
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=10, pady=5, fill="x")

        self.set_btn = tk.Button(
            btn_frame, text="설정", width=10, command=self._set_timer
        )
        self.set_btn.pack(side="left", padx=5)

        self.cancel_btn = tk.Button(
            btn_frame, text="취소", width=10, command=self._cancel_timer, state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=5)

        # ── 상태 표시 ──
        self.status_label = tk.Label(self.root, text="대기 중", fg="gray")
        self.status_label.pack(pady=5)

    def _capture_position(self):
        """3초 카운트다운 후 마우스 위치를 좌표에 입력"""
        self.capture_btn.config(state="disabled")

        def countdown():
            for i in range(3, 0, -1):
                self.root.after(0, lambda s=i: self.status_label.config(
                    text=f"{s}초 후 마우스 위치를 가져옵니다...", fg="orange"
                ))
                time.sleep(1)

            x, y = pyautogui.position()
            self.root.after(0, lambda: self._fill_coords(x, y))

        threading.Thread(target=countdown, daemon=True).start()

    def _fill_coords(self, x, y):
        self.x_entry.delete(0, "end")
        self.x_entry.insert(0, str(x))
        self.y_entry.delete(0, "end")
        self.y_entry.insert(0, str(y))
        self.status_label.config(text=f"좌표 입력됨: ({x}, {y})", fg="blue")
        self.capture_btn.config(state="normal")

    def _set_timer(self):
        if self.timer_active:
            messagebox.showwarning("경고", "이미 타이머가 설정되어 있습니다.")
            return

        try:
            target = datetime(
                int(self.year.get()), int(self.month.get()), int(self.day.get()),
                int(self.hour.get()), int(self.minute.get()), int(self.second.get()),
                int(self.ms.get()) * 1000,
            )
        except ValueError:
            messagebox.showerror("오류", "시간을 올바르게 입력하세요.")
            return

        x_str = self.x_entry.get().strip()
        y_str = self.y_entry.get().strip()
        if not x_str or not y_str:
            messagebox.showerror("오류", "좌표를 입력하세요.")
            return

        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            messagebox.showerror("오류", "좌표는 숫자로 입력하세요.")
            return

        try:
            click_count = int(self.count_entry.get().strip())
            delay_ms = int(self.delay_entry.get().strip())
        except ValueError:
            messagebox.showerror("오류", "횟수와 딜레이는 숫자로 입력하세요.")
            return

        diff = (target - datetime.now()).total_seconds()
        if diff < 0:
            messagebox.showwarning("경고", "목표 시간이 이미 지났습니다.")
            return

        self.timer_active = True
        self.set_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.status_label.config(
            text=f"대기 중... {target.strftime('%H:%M:%S.%f')[:-3]}에 ({x},{y}) 클릭",
            fg="green",
        )

        def wait_and_click():
            # 정밀 대기: 0.5초 전까지 sleep, 이후 busy-wait
            while self.timer_active:
                remaining = (target - datetime.now()).total_seconds()
                if remaining <= 0:
                    break
                if remaining > 0.5:
                    time.sleep(0.1)

            if not self.timer_active:
                return

            for i in range(click_count):
                pyautogui.click(x, y)
                if i < click_count - 1 and delay_ms > 0:
                    time.sleep(delay_ms / 1000)

            self.root.after(0, lambda: self._on_complete(click_count, x, y))

        threading.Thread(target=wait_and_click, daemon=True).start()

    def _on_complete(self, count, x, y):
        self.timer_active = False
        self.set_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(
            text=f"클릭 완료! ({x},{y})", fg="blue"
        )
        messagebox.showinfo("완료", f"({x}, {y}) 좌표에  클릭 완료!")

    def _cancel_timer(self):
        self.timer_active = False
        self.set_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.status_label.config(text="타이머 취소됨", fg="red")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ClickMacro().run()