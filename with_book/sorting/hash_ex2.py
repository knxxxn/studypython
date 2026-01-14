#상위 k번 이상 등장하는 요소를 추출하라
#입력: nums=[1,1,1,2,2,3], k=2    출력: [1,2]

def top_k(nums, k):
    count = {}

    for n in nums:
        if n in count:
            count[n] += 1
        else:
            count[n] = 1

    result = []
    for key, value in count.items():
        if value >= k:
            result.append(key)

    return result


#테스트용
nums = [1,1,1,2,2,3]
k = 2

print(top_k(nums, k))


from collections import Counter

def top_k_elements(nums, k):
    counter = Counter(nums)
    return [num for num, cnt in counter.items() if cnt >= k]