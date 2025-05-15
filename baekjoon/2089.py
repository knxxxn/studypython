# -2진수

n = int(input())
res=''
if n == 0:
    print(0)
    exit()

while n != 0:
    if n%-2:
        n = n//-2 + 1
        res = '1' + res
    else:
        n = n//-2
        res = '0' + res

print(res)