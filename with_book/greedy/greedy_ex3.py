#숫자 카드 게임

N,M = map(int,input().split())

result=0
for i in range(N):
    data = list(map(int,input().split()))
    a = min(data)
    result=max(result,a)

print(result)
