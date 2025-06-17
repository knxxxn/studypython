# 알고리즘 수업 - 깊이 우선 탐색 2

import sys

sys.setrecursionlimit(200000)  # 재귀 깊이 제한 증가
input = sys.stdin.readline  # 빠른 입력

n, m, r = map(int, input().split())
graph = [[] for _ in range(n + 1)]
visit = [False] * (n + 1)
order = [0] * (n + 1)
cnt = 0

# 간선 정보 입력
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)  # 무방향 그래프

for i in range(1, n + 1):
    graph[i].sort(reverse=True)


def dfs(start):
    global cnt
    visit[start] = True
    cnt += 1
    order[start] = cnt

    for next in graph[start]:
        if not visit[next]:
            dfs(next)


dfs(r)

for i in range(1, n + 1):
    print(order[i])