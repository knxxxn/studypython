#주어진 문자열이 팰린드롬인지 확인하라. 대소문자를 구분하지 않으며,영문자와 숫자만을 대상으로 한다.
# 팰린드롬 : 앞뒤가 똑같은 단어나 문장, 뒤집어도 같은 말이 되는 단어나 문장
import collections
from typing import Deque

def is_palindrome(s):
    chars = []

    for c in s:
        if c.isalnum():          # 영문자 + 숫자만
            chars.append(c.lower())

    while len(chars) > 1:
        if chars.pop(0) != chars.pop():
            return False

    return True

def is_palindrome(s):
    chars = []

    for c in s:
        if c.isalnum():
            chars.append(c.lower())

    return chars == chars[::-1]


def isPalindrome(self, s: str) -> bool: #리스트 풀이
    strs=[]
    for char in s:
        if char.isalnum():
            strs.append(char.lower())

    while len(strs) > 1: #팰린드롬 여부 판별
        if strs.pop(0) != strs.pop():
            return False

    return True

def isPalindrome(self, s: str) -> bool:
    # 자료형 데크로 선언
    strs: Deque = collections.deque()

    for char in s:
        if char.isalnum():
            strs.append(char.lower())

    while len(strs) > 1:
        if strs.popleft() != strs.pop():
            return False

    return True