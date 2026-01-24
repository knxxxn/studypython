#빨간색을 0, 흰색을 1, 파란색을 2라 할 때 순서대로 인접하는 제자리 정렬을 수행하라
#입력: [2,0,2,1,1,0] 출력: [0,0,1,1,2,2]

def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:  # 빨간색이면 왼쪽으로
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:  # 흰색이면 그대로 통과
            mid += 1
        else:  # 파란색이면 오른쪽으로
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums


# 테스트용
print(sortColors([2, 0, 2, 1, 1, 0]))