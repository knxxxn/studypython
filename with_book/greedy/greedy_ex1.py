#거스름돈 문제

N=int(input())

a=0
b=0
c=0
d=0

for i in range(N):
    a = N//500
    x = N%500
    b = x//100
    y = x%100
    c = y//50
    z = y%50
    d = z//10

print(a+b+c+d)
print(a)
print(b)
print(c)
print(d)

#답지
n=1260
count=0

coin_types = [500,100,50,10]

for coin in coin_types:
    count += n//coin #동전의 개수 세기
    n %= coin

print(count)