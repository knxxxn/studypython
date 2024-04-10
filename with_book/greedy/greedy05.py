#볼링공 고르기
N,M = map(int,input().split())
data=list(map(int,input().split()))

array=[0]*11 #1부터 10까지 무게를 넣을 수 있는 리스트
for x in data:
    array[x] += 1

result=0
for i in range(1,M+1):
    N -= array[i] #무게가 i인 볼링공의 개수(a가 선택할 수 있는 개수) 제외
    result += array[i] * N

print(result)