#이진 트리가 높이 균형인지 판단하라
#입력: [3,9,20,null,null,15,7]        [1,2,2,3,3,null,null,4,4]
#출력: true       false

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))

def isBalanced(root):
    if not root:
        return True

    left_h = height(root.left)
    right_h = height(root.right)

    if abs(left_h - right_h) > 1:
        return False

    return isBalanced(root.left) and isBalanced(root.right)


def dfs(node):
    if not node:
        return 0

    left = dfs(node.left)
    if left == -1:
        return -1

    right = dfs(node.right)
    if right == -1:
        return -1

    if abs(left - right) > 1:
        return -1

    return 1 + max(left, right) # 현재 노드 + 가장 깊은 자식 쪽 높이를 리턴

def isBalanced(root):
    return dfs(root) != -1
