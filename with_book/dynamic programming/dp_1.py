#피보나치 탑다운 방식

a = [0]*100 #메모이제이션을 위한 리스트 초기화

def fibo(x): #재귀함수를 사용한 방식
    if x == 1 or x == 2:
        return 1
    if a[x] != 0:
        return a[x]
    a[x] = fibo(x-1) + fibo(x-2)
    return a[x]

print(fibo(99))