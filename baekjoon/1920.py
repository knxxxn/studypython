#수 찾기
def binary_search(array, target, start, end):
    while start <= end:
        mid = (start + end) // 2
        if array[mid] == target:
            return mid
        elif array[mid] > target:
            end = mid - 1
        else:
            start = mid + 1
    return None

n = int(input())
A = list(map(int, input().split()))
m = int(input())
data = list(map(int, input().split()))

A.sort()

results = []
for query in data:
    result = binary_search(A, query, 0, n-1)
    if result is not None:
        results.append(1)
    else:
        results.append(0)

for result in results:
    print(result)

