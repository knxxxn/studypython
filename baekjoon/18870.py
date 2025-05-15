# 좌표 압축

import sys

n = int(sys.stdin.readline())
coordinates = list(map(int, sys.stdin.readline().split()))

# 중복을 제거하고 정렬된 좌표 목록 생성
# set(coordinates)로 중복을 제거
# sorted로 오름차순 정렬
sorted_coordinates = sorted(set(coordinates))

# 각 좌표에 대한 압축 결과(순위)를 저장할 딕셔너리 생성
# {원래 좌표: 압축된 값} 형태로 딕셔너리 저장
ranks = {}
for i, coord in enumerate(sorted_coordinates):
    ranks[coord] = i

# 각 원본 좌표에 대해 압축된 좌표(순위) 출력
result = []
for coord in coordinates:
    result.append(str(ranks[coord]))

print(' '.join(result))