#항목들을 조합하여 만들 수 있는 가장 큰 수를 출력하라
#입력: [10.2] 출력: 210
#입력: [3,30,34,5,9] 출력:9534330

from functools import cmp_to_key

def largestNumber(nums):
    # 모든 숫자를 문자열로 변환
    nums = list(map(str, nums))

    # 두 문자열을 더했을 때 더 큰 조합이 앞에 오도록 비교 함수 정의
    def compare(x, y):
        if x + y > y + x:
            return -1  # x가 앞으로
        elif x + y < y + x:
            return 1  # y가 앞으로
        else:
            return 0

    # 정렬 수행
    nums.sort(key=cmp_to_key(compare))

    # 결과가 '000'일 경우 '0'만 반환하도록 처리
    answer = str(int(''.join(nums)))
    return answer


# 테스트용
print(largestNumber([3, 30, 34, 5, 9]))