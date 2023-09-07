n = int(input())
m = list(map(int, input().split()))

m.sort()
a = 0
for i in range(n):
    for j in range(i+1):
        a += m[j]
        
print(a)