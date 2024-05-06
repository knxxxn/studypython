import googletrans
from os import linesep

translator = googletrans.Translator()

str1 = "행복하세요"
result1 = translator.translate(str1, dest='en', src='auto')
print(f"행복하세요 => {result1.text}")

str2 = "I am happy"
result2 = translator.translate(str2, dest='ko',src='en')
print(f"I am happy => {result2.text}")

#파일로된 문서 읽어서 번역하기
read_file_path = r"영어로된 파일.txt"

with open(read_file_path,'r') as f:
    readLines=f.readlines()

for lines in readLines:
    result = translator.translate(lines, dest='ko')
    print(result.txt)