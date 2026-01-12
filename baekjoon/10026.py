# 적록색약

n = int(input())
arr = [list(input().strip()) for _ in range(n)]

visited_normal = [[False]*n for _ in range(n)]

arr_rg = [row.copy() for row in arr]
for i in range(n):
    for j in range(n):
        if arr_rg[i][j] == 'G':
            arr_rg[i][j] = 'R'

def dfs(x, y, arr, visited):
    stack = [(x, y)]
    visited[x][y] = True
    color = arr[x][y]

    while stack:
        cx, cy = stack.pop()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < n:
                if not visited[nx][ny] and arr[nx][ny] == color:
                    visited[nx][ny] = True
                    stack.append((nx, ny))

# 일반인
count_normal = 0
for i in range(n):
    for j in range(n):
        if not visited_normal[i][j]:
            dfs(i, j, arr, visited_normal)
            count_normal += 1

# 적록색약
count_rg = 0
visited_rg = [[False]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if not visited_rg[i][j]:
            dfs(i, j, arr_rg, visited_rg)
            count_rg += 1

print(count_normal, count_rg)


