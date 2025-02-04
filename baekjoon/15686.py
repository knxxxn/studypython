#치킨 배달
from itertools import combinations #조합 사용

n, m = map(int, input().split())  # 도시 크기 n, 남길 치킨집 개수 m
city = [list(map(int, input().split())) for _ in range(n)]

# 집과 치킨집 위치 저장
houses = []
chickens = []

for i in range(n):
    for j in range(n):
        if city[i][j] == 1:  # 집 위치 저장
            houses.append((i, j))
        elif city[i][j] == 2:  # 치킨집 위치 저장
            chickens.append((i, j))

# 최소 치킨 거리 초기화
min_distance = float('inf')

# M개의 치킨집을 선택하는 모든 조합 탐색
for sel in combinations(chickens, m):
    total = 0  # 현재 조합의 치킨 거리 합

    # 모든 집에 대해 치킨 거리 계산
    for hx, hy in houses:
        min_dis = float('inf')  # 현재 집의 최소 치킨 거리
        for cx, cy in sel:
            distance = abs(hx - cx) + abs(hy - cy)  # 맨해튼 거리 계산
            min_dis = min(min_dis, distance)  # 최소 거리 갱신
        total += min_dis  # 모든 집의 거리 합산

    # 최소 치킨 거리 갱신
    min_distance = min(min_distance, total)

print(min_distance)
