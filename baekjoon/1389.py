# 케빈 베이컨의 6단계 법칙

import sys
from collections import deque

def bfs(start, graph, n):
    # 각 유저까지의 거리를 저장할 리스트
    distance = [0] * (n + 1)
    # 방문 여부를 체크할 리스트
    visited = [False] * (n + 1)
    
    # BFS를 위한 큐 생성
    queue = deque([start])
    visited[start] = True
    
    while queue:
        current = queue.popleft()
        # 현재 노드와 연결된 모든 노드에 대해
        for next_node in graph[current]:
            if not visited[next_node]:
                # 거리 계산
                distance[next_node] = distance[current] + 1
                visited[next_node] = True
                queue.append(next_node)
    
    # 모든 거리의 합 반환
    return sum(distance)

def main():
    # 입력 받기
    n, m = map(int, sys.stdin.readline().split())
    
    # 그래프 초기화 (인접 리스트)
    graph = [[] for _ in range(n + 1)]
    
    # 친구 관계 입력 받기
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        graph[a].append(b)
        graph[b].append(a)
    
    # 각 유저의 케빈 베이컨 수 계산
    min_bacon = float('inf')
    min_user = 0
    
    for i in range(1, n + 1):
        bacon = bfs(i, graph, n)
        if bacon < min_bacon:
            min_bacon = bacon
            min_user = i
    
    print(min_user)

if __name__ == "__main__":
    main()

# 인접 행렬을 사용한 풀이
def bfs_matrix(start, matrix, n):
    distance = [0] * (n + 1)
    visited = [False] * (n + 1)
    
    queue = deque([start])
    visited[start] = True
    
    while queue:
        current = queue.popleft()
        # 인접 행렬에서 연결된 노드 찾기
        for next_node in range(1, n + 1):
            # 연결되어 있고 방문하지 않은 노드라면
            if matrix[current][next_node] == 1 and not visited[next_node]:
                distance[next_node] = distance[current] + 1
                visited[next_node] = True
                queue.append(next_node)
    
    return sum(distance)

def main_matrix():
    n, m = map(int, sys.stdin.readline().split())
    
    # 인접 행렬 초기화 (N+1 x N+1 크기의 2차원 배열)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    # 친구 관계 입력 받기
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        matrix[a][b] = 1  # a와 b가 연결됨
        matrix[b][a] = 1  # 양방향 그래프이므로 b와 a도 연결됨
    
    # 각 유저의 케빈 베이컨 수 계산
    min_bacon = float('inf')
    min_user = 0
    
    for i in range(1, n + 1):
        bacon = bfs_matrix(i, matrix, n)
        if bacon < min_bacon:
            min_bacon = bacon
            min_user = i
    
    print(min_user)

# 인접 행렬 풀이 실행
# if __name__ == "__main__":
#     main_matrix()

