#상범 빌딩
from collections import deque

directions = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

def read_input():
    cases = []
    while True:
        l, r, c = map(int, input().split())
        if l == 0 and r == 0 and c == 0:
            break
        building = []
        start, end = None, None
        for i in range(l):
            floor = [list(input().strip()) for _ in range(r)]
            building.append(floor)
            for x in range(r):
                for y in range(c):
                    if floor[x][y] == 'S':
                        start = (i, x, y)
                    elif floor[x][y] == 'E':
                        end = (i, x, y)
            input()
        cases.append((l, r, c, building, start, end))
    return cases

def bfs(l, r, c, building, start, end):
    queue = deque([(*start, 0)])
    visited = [[[False] * c for _ in range(r)] for _ in range(l)]
    visited[start[0]][start[1]][start[2]] = True

    while queue:
        z, x, y, time = queue.popleft()
        if (z, x, y) == end:
            return f"Escaped in {time} minute(s)."
        for dz, dx, dy in directions:
            nz, nx, ny = z + dz, x + dx, y + dy

            if 0 <= nz < l and 0 <= nx < r and 0 <= ny < c:
                if not visited[nz][nx][ny] and building[nz][nx][ny] in ('.', 'E'):
                    visited[nz][nx][ny] = True
                    queue.append((nz, nx, ny, time + 1))
    return "Trapped!"

cases = read_input()
for l, r, c, building, start, end in cases:
    if start and end:
        print(bfs(l, r, c, building, start, end))
    else:
        print("Trapped!")
