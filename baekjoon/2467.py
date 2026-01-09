#용액

n = int(input())
arr = list(map(int, input().split()))

left = 0
right = n - 1
min_abs = float('inf')
result_l, result_r = 0, 0

while left < right:
    sum_val = arr[left] + arr[right]

    if abs(sum_val) < min_abs:
        min_abs = abs(sum_val)
        result_l, result_r = arr[left], arr[right]

    if sum_val > 0:
        right -= 1
    elif sum_val < 0:
        left += 1
    else:
        break

print(result_l, result_r)