#두 수의 합
import sys

input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))
x = int(input())

seen = set()
count = 0

for num in nums:
    need = x - num
    if need in seen:
        count += 1
    seen.add(num)

print(count)