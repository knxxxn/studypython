#만들 수 없는 금액
N=int(input())
data=list(map(int,input().split()))
data.sort()

money = 1

for x in data:
    if money < x:
        break
    money += x

print(money)

