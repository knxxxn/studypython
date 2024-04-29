from gtts import gTTS
from playsound import playsound
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) #경로를 .py파일의 실행경로로 이동, 현재 경로로 이동
text = "안녕하세요"

tts=gTTS(text=text, lang='ko')
tts.save("hi.mp3")

playsound("hi.mp3")

file_path='나의 텍스트.txt' #파일에서 문자를 읽어 음성으로 출력하기
with open(file_path,'rt',encoding='UTF8')as f:
    read_file = f.read()

tts = gTTS(text=read_file,lang='ko')
tts.save("myText.mp3")

playsound("myText.mp3")
