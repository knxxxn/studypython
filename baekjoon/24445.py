# 알고리즘 수업 - 너비 우선 탐색 2

from collections import deque
import sys

input = sys.stdin.readline

n, m, r = map(int, input().split())

graph = [[] for _ in range(n + 1)]
visited = [False] * (n + 1)
order = [0] * (n + 1)

# 간선 정보 입력
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

for i in range(1, n + 1):
    graph[i].sort(reverse=True)

# BFS
queue = deque([r])
visited[r] = True
cnt = 1
order[r] = cnt

while queue:
    v = queue.popleft()
    for i in graph[v]:  # 정렬된 리스트 사용
        if not visited[i]:
            queue.append(i)
            visited[i] = True
            cnt += 1
            order[i] = cnt

# 출력
for i in range(1, n + 1):
    print(order[i])
