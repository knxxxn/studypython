#모험가 길드

N=int(input())
data=list(map(int,input().split()))
data.sort()

group=0 #그룹 수
member=0 #모험가 수

for i in data:
    group+=1
    if group >= i:
        member += 1
        group = 0 #현재 그룹에 포함된 모험가의 수 초기화

print(group)