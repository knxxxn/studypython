#왕실의 나이트

data = input()
row = int(data[1])
col = int(ord(data[0]))-int(ord('a')) + 1

move = [(-2,1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]

result = 0
for i in move:
    move_row = row + i[0]
    move_col = col + i[1]

    if move_row >= 1 and move_row <=8 and move_col >= 1 and move_col <= 8:
        result += 1

print(result)