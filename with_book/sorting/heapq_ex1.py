#k개의 정렬된 리스트르 ㄹ1개의 정렬된 리스트로 병합하라
#입력: [1->4->5   1->3->4    2->6]    출력: [1->1->2->3->4->4->5->6]

import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeKLists(lists):
    heap = []

    # 각 리스트의 첫 노드를 힙에 넣기
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    cur = dummy

    # 힙에서 하나씩 꺼내 병합
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


# 테스트용
def build_linked_list(arr):
    dummy = ListNode()
    cur = dummy

    for x in arr:
        cur.next = ListNode(x)
        cur = cur.next

    return dummy.next

def print_linked_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    print(result)

l1 = build_linked_list([1, 4, 5])
l2 = build_linked_list([1, 3, 4])
l3 = build_linked_list([2, 6])

lists = [l1, l2, l3]

result = mergeKLists(lists)
print_linked_list(result)
