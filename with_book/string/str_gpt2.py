'''
문제 2️⃣ : 정렬된 배열에서 제곱의 합 찾기
📘 문제
정렬된 정수 배열이 주어진다.
서로 다른 두 수의 제곱의 합이 target이 되면 True를 반환하라.
🧩입력
nums = [-4, -2, 1, 3, 5]
target = 25
🧩출력
True
(예: 3² + 4² = 9 + 16 = 25)
'''

'''
left, right = 0, len(s) - 1
while left < right:
    s[left], s[right] = s[right], s[left]
'''

def square_sum(nums, target):
    left, right = 0, len(nums) - 1

    while left < right:
        total = nums[left]**2 + nums[right]**2

        if total == target:
            return True
        elif total < target:
            left += 1
        else:
            right -= 1

    return False
