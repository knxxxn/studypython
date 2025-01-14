#토마토
from collections import deque

n, m = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(m)]
dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs():
    queue = deque()

    for i in range(m): # 익은 토마토(1)를 큐에 추가
        for j in range(n):
            if graph[i][j] == 1:
                queue.append((i, j))
    while queue:
        x, y = queue.popleft()
        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n and graph[nx][ny] == 0: #유효 범위 내에서 익지 않은 토마토(0)만 처리
                graph[nx][ny] = graph[x][y] + 1
                queue.append((nx, ny))
bfs()

max_days = 0
for row in graph:
    if 0 in row:  #익지 않은 토마토(0)가 남아 있을 때
        print(-1)
        break
    max_days = max(max_days, max(row))
else:
    print(max_days - 1)  #날짜 출력
