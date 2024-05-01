#시각

N = int(input())
c=0

for i in range(N+1):
    for j in range(60):
        for k in range(60):
            if str(N) in str(i) + str(j) + str(k):
                c += 1

print(c)