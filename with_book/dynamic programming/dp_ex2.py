#당신은 계단을 오르고 있다. 정상에 도달하기 위해 n 계단을 올라야 한다. 매번 각각 1계단 또는 2계단씩 오를 수 있다면 정상에 도달하기 위한 방법은 몇 가지 경로가 되는지 계산하라
#입력: 3      출력: 3

#이거 타임아웃 발생
def stair(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return stair(n-1) + stair(n-2)

#메모이제이션
def stair(n, memo={}):
    if n in memo:
        return memo[n]

    if n == 1:
        return 1
    if n == 2:
        return 2

    memo[n] = stair(n-1, memo) + stair(n-2, memo)
    return memo[n]

#바텀업
def stair(n):
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]
