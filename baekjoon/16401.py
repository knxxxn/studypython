#과자 나눠주기

m, n = map(int, input().split())
snack = list(map(int, input().split()))

start = 1  # 간식 길이의 최소값
end = max(snack)  # 간식의 가장 긴 길이
res = 0  # 조건을 만족하는 간식 길이의 최댓값

while start <= end:
    mid = (start + end) // 2
    total = 0  # 이 길이로 간식을 잘랐을 때 얻을 수 있는 간식의 총 개수

    for i in snack:
        if i >= mid:
            total += i // mid
            # 간식 하나씩 확인하면서 현재 mid 길이로 나누었을 때 얻을 수 있는 간식 개수를 계산
            # 간식의 길이 i가 mid보다 짧으면 나눌 수 없으므로 건너뜀

    if total >= m:
        res = mid
        start = mid + 1
    else:
        end = mid - 1

        # total >= m: 모두 간식을 줄 수 있다면 더 긴 길이를 위해 start를 증가
    # total < m: 간식 길이가 너무 길어서 나눌 수 없다면 end를 감소

print(res)

