#1로 만들기 2
n = int(input())

# DP 테이블과 경로 저장 테이블 초기화
dp = [0] * (n + 1)
path = [0] * (n + 1)

for i in range(2, n + 1):
    # 기본 연산 (i-1)
    dp[i] = dp[i - 1] + 1
    path[i] = i - 1

    # 2로 나누어 떨어질 때
    if i % 2 == 0 and dp[i] > dp[i // 2] + 1:
        dp[i] = dp[i // 2] + 1
        path[i] = i // 2

    # 3으로 나누어 떨어질 때
    if i % 3 == 0 and dp[i] > dp[i // 3] + 1:
        dp[i] = dp[i // 3] + 1
        path[i] = i // 3

# 최소 연산 횟수 출력
print(dp[n])

# 경로 역추적
result = []
while n != 0:
    result.append(n)
    n = path[n]

print(*result) # 언패킹: 리스트의 요소를 개별적으로 꺼내어 출력

