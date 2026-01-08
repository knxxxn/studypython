#덧셈하여 타겟을 만들 수 있는 배열의 두 숫자 인덱스를 리턴하라
#입력: nums = [2,7,11,15] target = 9
#출력: [0,1]

def two_sum(nums, target):
    s = {}  # 값: 인덱스

    for i, num in enumerate(nums):
        need = target - num
        if need in s:
            return [s[need], i]
        s[num] = i

# 테스트용
print(two_sum([2,7,11,15], 9))