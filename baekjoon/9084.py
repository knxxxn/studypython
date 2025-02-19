#동전

def coin_change():
    T = int(input())  # 테스트 케이스 개수

    for _ in range(T):
        N = int(input())  # 동전 종류 개수
        coins = list(map(int, input().split()))  # 동전 리스트
        M = int(input())  # 목표 금액

        dp = [0] * (M + 1)
        dp[0] = 1  # 0원을 만드는 방법 1가지

        for coin in coins:  # 동전 하나씩 확인
            for i in range(coin, M + 1):  # 현재 동전을 사용해 만들 수 있는 금액들 갱신
                dp[i] += dp[i - coin]

        print(dp[M])  # 목표 금액을 만드는 방법의 수 출력

coin_change()
