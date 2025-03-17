#오토 마우스를 활용한 자동화

import threading
import time

import pyautogui
import os

import pyperclip
import schedule

os.chdir(os.path.dirname(os.path.abspath(__file__)))
picPosition = pyautogui.locateOnScreen('pic1.png')
print(picPosition)

if picPosition is None:
    picPosition = pyautogui.locateOnScreen('pic2.png')
    print(picPosition)

clickPosition = pyautogui.center(picPosition)
pyautogui.doubleClick(clickPosition)

pyperclip.copy("이 메세지는 자동으로 보내는 메세지 입니다")
pyautogui.hotkey("ctrl","v")
time.sleep(1.0)

pyautogui.write(["enter"])
time.sleep(1.0)

pyautogui.write(["escape"])
time.sleep(1.0)

def send_message():
    threading.Timer(10,send_message).start()
    picPosition = pyautogui.locateOnScreen('pic1.png')
    print(picPosition)

schedule.every(10).second.do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)