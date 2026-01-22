#정렬되지 않은 배열에서 k번째 큰 요소를 추출하라
#입력: [3,2,3,1,2,4,5,5,6], k=4
#출력 : 4


nums = [3,2,3,1,2,4,5,5,6]
k = 4


#sort 사용
def sorting(nums, k):

    n = sorted(nums, reverse=True)
    answer = n[k-1] #인덱스는 0부터 시작이니까

    return answer

print(sorting(nums, k))

#heapq 사용
import heapq

def kth_largest(nums, k):
    heap = []

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]

print(kth_largest(nums, k))
