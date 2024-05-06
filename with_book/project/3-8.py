#메인코드가 동작할 때에만 쓰레드 동작하는 코드
import threading
import time

def thread_1():
    while True:
        print("쓰레드1 동작")
        time.sleep(1.0)

t1 = threading.Thread(target=thread_1())
t1.daemon = True
t1.start()

while True:
    print("메인동작")
    time.sleep(2.0)

#다수의 쓰레드를 동작시키는 코드
import threading

def sum(name, value):
    for i in range(0, value):
        print(f"{name} : {i}")

t1 = threading.Thread(target=sum, args=('1번 스레드', 10))
t2 = threading.Thread(target=sum, args=('2번 스레드', 10))

t1.start()
t2.start()

print('main thread')