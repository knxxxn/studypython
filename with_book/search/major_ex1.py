#과반수를 차지하는 엘리먼트를 출력하라
#입력: [3,2,3]    #출력: 3

from collections import Counter

def major(nums):
    counter = Counter(nums)
    for num, cnt in counter.items():
        if cnt > len(nums) // 2:
            return num

#테스트용
print(major([3,2,3]))


#분할정복 코드
def majorityElement(nums):
    def divide(lo, hi):
        # 원소가 하나면 그 자체가 과반수 후보
        if lo == hi:
            return nums[lo]

        mid = (lo + hi) // 2
        left = divide(lo, mid)
        right = divide(mid + 1, hi)

        if left == right:
            return left

        left_count = sum(1 for i in range(lo, hi + 1) if nums[i] == left)
        right_count = sum(1 for i in range(lo, hi + 1) if nums[i] == right)

        return left if left_count > right_count else right

    return divide(0, len(nums) - 1)
