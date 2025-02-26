#트럭

from collections import deque
import sys

def bridge_simulation(n, w, L, trucks):
    bridge = deque([0] * w)  #다리 길이만큼 0으로 채운 큐 (트럭이 없으면 0)
    truck_index = 0  #다음에 올라올 트럭의 인덱스
    total_weight = 0  #현재 다리 위 트럭들의 총 무게
    time = 0  #걸리는 시간

    while truck_index < n or total_weight > 0:
        time += 1  #시간 1초 증가
        #다리 맨 앞에서 트럭이 빠져나감
        total_weight -= bridge.popleft()

        # 다음 트럭이 올라갈 수 있는지 확인
        if truck_index < n and total_weight + trucks[truck_index] <= L:
            bridge.append(trucks[truck_index])  #새로운 트럭 추가
            total_weight += trucks[truck_index]
            truck_index += 1  #다음 트럭으로 이동
        else:
            bridge.append(0)  #트럭이 못 올라가면 빈 공간 추가

    return time  #모든 트럭이 지나가는 데 걸린 시간 반환

n, w, L = map(int, sys.stdin.readline().split())  #트럭 수, 다리 길이, 최대 하중
trucks = list(map(int, sys.stdin.readline().split()))  #트럭들의 무게 리스트

print(bridge_simulation(n, w, L, trucks))
