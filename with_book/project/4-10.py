import pyautogui
import time
import pyperclip

#마우스의 좌표를 출력하는 코드
while True:
    print(pyautogui.position())
    time.sleep(0.1)

#네이버에서 자동으로 서울 날씨 검색하는 코드 만들기
pyautogui.moveTo(1241,206,0.2)
pyautogui.click()
time.sleep(0.5)

pyperclip.copy("서울 날씨")
pyautogui.hotkey("ctrl","v")
time.sleep(0.5)

pyautogui.write(["enter"])
time.sleep(1)

start_x = 992
start_y = 220
end_x = 1656
end_y = 635 # 시작 x,y좌표 및 종료 x,y좌표를 입력

pyautogui.screenshot(r'서울날씨.png', region=(start_x, start_y, end_x-start_x, end_y-start_y))