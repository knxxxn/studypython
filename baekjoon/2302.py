#극장 좌석

fib = [1] * 41 # 피보나치 DP 테이블 (최대 40까지)
for i in range(2, 41):
    fib[i] = fib[i - 1] + fib[i - 2]

n = int(input())  # 좌석 개수
m = int(input())  # VIP 개수
vip = [int(input()) for _ in range(m)]  # VIP 좌석 목록

# VIP를 기준으로 나누어 경우의 수 계산
result = 1
prev = 0  # VIP 좌석 전까지의 구간 시작점

for v in vip:
    length = v - prev - 1  # VIP까지의 좌석 길이
    result *= fib[length]  # 해당 구간의 경우의 수 곱하기
    prev = v  # 이전 VIP 갱신

# 마지막 구간도 처리
length = n - prev  # 마지막 VIP 이후 구간의 좌석 수
result *= fib[length] #이 구간에서 자리 변경 가능한 경우의 수를 구하고 기존 값에 곱함

print(result)
