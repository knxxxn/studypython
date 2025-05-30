# 에디터

import sys

input = sys.stdin.readline

s = input().strip() #문자열 입력
n = int(input().strip()) #명령어 개수, int(s)로 하면 int(문자열)이 되서 에러 남

left = list(s)  # 커서 왼쪽 문자들
right = []  # 커서 오른쪽 문자들 (뒤집어서 저장)

for _ in range(n):
    cmd = input().strip().split()

    if cmd[0] == 'L':  # 커서를 왼쪽으로
        if left:
            right.append(left.pop())

    elif cmd[0] == 'D':  # 커서를 오른쪽으로
        if right:
            left.append(right.pop())

    elif cmd[0] == 'B':  # 커서 왼쪽 문자 삭제
        if left:
            left.pop()

    elif cmd[0] == 'P':  # 커서 왼쪽에 문자 추가
        left.append(cmd[1])

print(''.join(left) + ''.join(reversed(right)))