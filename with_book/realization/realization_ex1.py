#상하좌우

N = int(input())
route = input().split()

x, y = 1, 1

# 이동 방향에 따른 좌표 변화
route_x = [0, 0, -1, 1]
route_y = [-1, 1, 0, 0]
move = ['L', 'R', 'U', 'D']

for i in route:
    if i == 'L':
        move_x, move_y = x + route_x[0], y + route_y[0]
    elif i == 'R':
        move_x, move_y = x + route_x[1], y + route_y[1]
    elif i == 'U':
        move_x, move_y = x + route_x[2], y + route_y[2]
    elif i == 'D':
        move_x, move_y = x + route_x[3], y + route_y[3]

    if move_x < 1 or move_y < 1 or move_x > N or move_y > N:
        continue

    x, y = move_x, move_y

print(x, y)


