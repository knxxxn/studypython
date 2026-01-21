#이진 트리의 최대 깊이를 구하라
#입력: [3,9,20,null,null,15,7]
#출력: 3

import collections

# 1) TreeNode 정의
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# 2) 배열 → 트리로 변환
def build_tree(arr):
    if not arr or arr[0] is None:
        return None

    nodes = [None if v is None else TreeNode(v) for v in arr]

    for i in range(len(arr)):
        if nodes[i] is None:
            continue

        left_idx = 2*i + 1
        right_idx = 2*i + 2

        if left_idx < len(arr):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(arr):
            nodes[i].right = nodes[right_idx]

    return nodes[0]

root_arr = [3,9,20,None,None,15,7]
root = build_tree(root_arr)

# 3) BFS로 최대 깊이
def maxDepth(root) -> int:
    if root is None:
        return 0

    queue = collections.deque([root])
    depth = 0

    while queue:
        depth += 1
        for _ in range(len(queue)):
            cur = queue.popleft()
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)

    return depth

#BFS 반복횟수 == 깊이
print(maxDepth(root))
