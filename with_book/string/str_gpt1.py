'''
문제 1️⃣ : 유효한 팰린드롬 (투 포인터 심화)
📘 문제
주어진 문자열에서 영문자와 숫자만 고려하고
대소문자를 무시했을 때 팰린드롬이면 True, 아니면 False를 반환하라.
🧩입력
"No lemon, no melon"
🧩출력
True
'''

'''
left, right = 0, len(s) - 1
while left < right:
    s[left], s[right] = s[right], s[left]
'''

def is_palindrome_two_pointer(s):
    left, right = 0, len(s) - 1

    while left < right:
        if not s[left].isalnum(): # 왼쪽이 유효 문자가 아니면 건너뜀
            left += 1
            continue

        if not s[right].isalnum(): # 오른쪽이 유효 문자가 아니면 건너뜀
            right -= 1
            continue

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
