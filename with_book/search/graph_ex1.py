#1을 육지로 0을 물로 가정한 2D 그리드 맵이 주어졌을 때, 섬의 개수를 계산해라(연결되어있는 1의 덩어리 개수를 구하라)
#입력
'''
11110       11000
11010       11000
11000       00100
00000       00011
'''
#출력 1       3

#DFS 버전
def islands_dfs(grid):
    if not grid:
        return 0

    n = len(grid)
    m = len(grid[0])
    count = 0

    def dfs(x, y):
        # 범위 체크 + 물이면 종료
        if x < 0 or x >= n or y < 0 or y >= m or grid[x][y] == 0:
            return

        # 방문 처리
        grid[x][y] = 0

        # 상하좌우 탐색
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                dfs(i, j)
                count += 1

    return count

#BFS 버전
from collections import deque

def islands_bfs(grid):
    if not grid:
        return 0

    n = len(grid)
    m = len(grid[0])
    count = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                count += 1
                queue = deque([(i, j)])
                grid[i][j] = 0  # 방문 처리

                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 1:
                            grid[nx][ny] = 0
                            queue.append((nx, ny))

    return count


#테스트용
import copy

grid = [
    [1,1,1,1,0],
    [1,1,0,1,0],
    [1,1,0,0,0],
    [0,0,0,0,0]
]

print(islands_dfs(copy.deepcopy(grid)))
print(islands_bfs(copy.deepcopy(grid)))
