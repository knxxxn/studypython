# N번째 큰 수

# 1번째
import heapq
import sys

n = int(sys.stdin.readline())
heap = []

for i in range(n):
    a = list(map(int, sys.stdin.readline().split()))

    if not heap:  # 리스트가 비어있으면 모든 값을 넣음
        for j in a:
            heapq.heappush(heap, j)
    else:
        for j in a:
            if heap[0] < j:  # 새 값 리스트[0]보다 최솟값보다 크면
                heapq.heappush(heap, j)  # 새 값을 추가
                heapq.heappop(heap)  # 있던거 없애기

    # n개만 유지
    while len(heap) > n:
        heapq.heappop(heap)

print(heap[0])

# 2번째
import heapq
import sys
from heapq import nlargest

n = int(input())
heap = []

for i in range(n):
    row = list(map(int, input().split()))
    for j in row:
        heap.append(j)

find = nlargest(n, heap)
print(find[n-1])

# 3번째
import heapq
import sys

n = int(input())
heap = []

for i in range(n):
    row = list(map(int, input().split()))

    for num in row:
        heapq.heappush(heap, num) #값 추가
        if len(heap) > n:
            heapq.heappop(heap) # n을 초과하면 가장 작은 값 제거

print(heap[0]) #리스트에 가장 작은 값이 n번째로 큰 값임
