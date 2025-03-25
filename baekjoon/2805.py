#나무 자르기

def solve():
    n, m = map(int, input().split())
    trees = list(map(int, input().split()))

    start = 0
    end = max(trees)
    result = 0

    while start <= end:
        mid = (start + end) // 2
        total = 0

        for tree in trees:
            if tree > mid:
                total += tree - mid

        if total >= m:
            result = mid
            start = mid + 1
        else:
            end = mid - 1

    print(result)

solve()

#2번째 방법
n, m = map(int,input().split())
tree = list(map(int, input().split()))

start = 0
end = max(tree)
res = 0
while start <= end:
    mid = (start + end)//2
    total = 0

    for i in tree:
        if i > mid:
            total += i - mid

    if total >= m:
        res = mid
        start = mid + 1
    else:
        end = mid - 1

print(res)
