#높이를 입력받아 비 온 후 얼마나 많은 물이 쌓일 수 있는지를 계산하라
#입력: [0,1,0,2,1,0,1,3,2,1,2,1]
#출력: 6

def rain(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water

#테스트용
print(rain([0,1,0,2,1,0,1,3,2,1,2,1]))