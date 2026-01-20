'''
아래 미로에서 0→1로 가는 최소 이동 횟수 구하기
0 1 0
0 0 0
1 0 1
'''

from collections import deque

maze = [
    [0,1,0],
    [0,0,0],
    [1,0,1]
]

n, m = 3, 3
visited = [[False]*m for _ in range(n)]

def bfs():
    q = deque()
    q.append((0,0,0))  # x, y, 거리
    visited[0][0] = True

    while q:
        x, y, dist = q.popleft()

        if maze[x][y] == 1:
            return dist

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny, dist+1))

    return -1

print(bfs())