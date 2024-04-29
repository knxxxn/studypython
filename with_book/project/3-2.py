import socket
import requests
import re

#내부 ip
in_addr = socket.gethostbyname(socket.gethostname())
in_addr2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
in_addr2.connect(("www.google.co.kr",443))

'''
print(in_addr)
print(in_addr2.getsockname()[0]) #in_addr과 결과값 동일

'''
#외부 ip
req = requests.get("http://ipconfig.kr")
out_addr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',req.text)[1]

print("내부 ip : ",in_addr2.getsockname()[0])
print("외부 ip : ", out_addr)