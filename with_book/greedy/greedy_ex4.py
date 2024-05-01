#1이 될 때까지

N,K = map(int,input().split())
n = 0

while N >= K :
    if N % K != 0:
            N-=1
            n+=1
    else :
            N //= K
            n+=1

n += N-1
print(n)



