#문자열 S와 T를 입력받아 O(n)에 T의 모든 문자가 포함된 S의 최소 윈도우를 찾아라
#입력: S="ABOBECODEBANC", T="ABC"
#출력: "BANC"

from collections import Counter

def slicing(S, T):
    if not S or not T:
        return ""

    need = Counter(T)       # T에 필요한 문자 수
    window = {}
    required = len(need)   # 충족해야 할 문자 종류 수
    formed = 0             # 현재 충족된 문자 종류 수

    left = 0
    min_len = float("inf")
    min_window = ""

    for right in range(len(S)):
        char = S[right]
        window[char] = window.get(char, 0) + 1

        # 필요한 문자이고, 필요한 개수를 정확히 맞췄을 때
        if char in need and window[char] == need[char]:
            formed += 1

        # 모든 문자가 충족되었으면 윈도우 줄이기
        while formed == required:
            # 최소 길이 갱신
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = S[left:right + 1]

            # 왼쪽 포인터 이동
            left_char = S[left]
            window[left_char] -= 1

            if left_char in need and window[left_char] < need[left_char]:
                formed -= 1

            left += 1

    return min_window


# 테스트
print(slicing("ABOBECODEBANC", "ABC")) 
