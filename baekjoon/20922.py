#겹치는 건 싫어

#1번
n, k = map(int, input().split())
a = list(map(int, input().split()))
start = 0
end = 0
res = [0] * (max(a) + 1)
max_length = 0

while end < n:
    if res[a[end]] < k:
        res[a[end]] += 1
        end += 1
        max_length = max(max_length, end - start)
    else:
        res[a[start]] -= 1
        start += 1

print(max_length)

#2번
def solve():
    # 입력 받기
    n, k = map(int, input().split())  # n: 배열의 길이, k: 각 원소의 최대 허용 반복 횟수
    a = list(map(int, input().split()))  # 입력 배열

    start = 0  # 윈도우의 시작 지점
    end = 0  # 윈도우의 끝 지점

    # 배열의 최대값 + 1 크기의 카운터 배열 생성
    # 각 원소의 등장 횟수를 추적
    res = [0] * (max(a) + 1)

    # 최대 부분 배열의 길이를 저장할 변수
    max_length = 0

    # 슬라이딩 윈도우 알고리즘
    while end < n:
        # 현재 원소의 등장 횟수가 m보다 작으면
        if res[a[end]] < k:
            # 해당 원소의 카운터 증가
            res[a[end]] += 1
            # 윈도우 끝 지점 이동
            end += 1
            # 현재 윈도우 길이와 기존 최대 길이 비교
            max_length = max(max_length, end - start)
        else:
            # 현재 원소의 등장 횟수가 m을 초과하면
            # 윈도우 시작 지점의 원소 카운터 감소
            res[a[start]] -= 1
            # 윈도우 시작 지점 이동
            start += 1

    # 최종 최대 길이 출력
    print(max_length)


solve()
