#DFS와 BFS
from collections import deque

n, m, v = map(int, input().split())
graph = [[] for i in range(n + 1)]

visit_dfs = [False] * (n + 1)
visit_bfs = [False] * (n + 1)

for i in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for i in graph:
    i.sort()


def dfs(start):
    print(start, end=' ')
    visit_dfs[start] = True
    for next in graph[start]:
        if not visit_dfs[next]:
            dfs(next)


def bfs(start):
    queue = deque()
    queue.append(start)
    visit_bfs[start] = True

    while queue:
        k = queue.popleft()
        print(k, end=' ')
        for next in graph[k]:
            if not visit_bfs[next]:
                queue.append(next)
                visit_bfs[next] = True


dfs(v)
print()
bfs(v)