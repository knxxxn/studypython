#중복된 문자를 제외하고 사전식 순서로 나열하라
#입력: bcabc  출력: abc


def removeLetter(s):
    return "".join(sorted(set(s)))

#테스트
print(removeLetter("babac"))