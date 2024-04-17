#큰 수의 법칙

N,M,K = map(int,input().split())
data = list(map(int,input().split()))

data.sort()
a=data[N-1]
b=data[N-2]

result = 0

while True:
    for i in range(K):
        if M == 0:
            break
        result += a
        M -= 1
    if M == 0:
        break
    result += b
    M -= 1

print(result)





