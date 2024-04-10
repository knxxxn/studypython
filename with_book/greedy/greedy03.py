#문자열 뒤집기
data=input()

zero=0 # 0으로 바꾸는 경우
one=0 # 1로 바꾸는 경우

#첫번째 원소에 대해 처리
if data[0] == '1':
    zero+=1
else:
    one+=1

#두번째 원소부터 모든 원소를 확인
for i in range(len(data)-1):
    if data[i] != data[i+1]:
        if data[i+1] == '1': #다음수에서 1로 바뀌는 경우
            zero += 1
        else: #0으로 바뀌는 경우
            one += 1

print(min(zero,one))