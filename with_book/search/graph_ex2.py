#숫자 집합 candidates를 조합하여 합이 target이 되는 원소를 나열하라. 각 원소는 중복으로 나열 가능하다.
#입력:candidates=[2,3,6,7], targets = 7
#출력: [[7],[2,2,3]]

def combinationSum(candidates, target):
    result = []

    def dfs(start, remain, path):
        if remain == 0:
            result.append(path[:])
            return
        if remain < 0:
            return

        for i in range(start, len(candidates)):
            path.append(candidates[i])
            dfs(i, remain - candidates[i], path)
            path.pop()

    dfs(0, target, [])
    return result

#테스트용
candidates = [2,3,6,7]
target = 7
print(combinationSum(candidates,target))