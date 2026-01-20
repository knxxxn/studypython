'''
그래프와 시작점이 주어질 때, 모든 정점을 한 번씩 방문하는 경로를 구하라.
graph = {
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["D", "B"],
  "D": []
}
start = "A"
'''

graph = {
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["D", "B"],
  "D": []
}

start = "A"

def dfs(path, visited):
    if len(path) == len(graph):
        print(path)
        return

    cur = path[-1]
    for nxt in graph[cur]:
        if nxt not in visited:
            visited.add(nxt)
            dfs(path + [nxt], visited)
            visited.remove(nxt)

dfs([start], {start})
