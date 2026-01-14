#J는 보석이며, S는 갖고 있는 돌이다. S에는 보석이 몇개나 있을까? 대소문자는 구분한다.
#입력: J="aA", S="aAAbbbb"        출력: 3

def countJ(J, S):
    count = 0
    for s in S:
        if s in J:
            count += 1
    return count


#테스트용
J = "aA"
S = "aAAbbbb"

print(countJ(J, S))



def count_jewels(jewels, stones):
    jewel_set = set(jewels)
    return sum(1 for s in stones if s in jewel_set)



J = "aA"
S = "aAAbbbb"

print(sum(1 for s in S if s in J))