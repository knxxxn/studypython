#퀵 정렬
array = [7,5,9,0,3,1,6,2,4,8]

def quick_sort(array):
    if len(array) <= 1: #리스트가 하나 이하의 원소만을 담고 있다면 종료
        return array

    pivot = array[0]
    tail = array[1:]

    left = [x for x in tail if x <= pivot]
    right = [x for x in tail if x > pivot]

    return quick_sort(left) + pivot + quick_sort(right)

print(quick_sort(array))