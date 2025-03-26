# 리스트에서 인접하지 않는 인자들을 선정하여 최대합 계산
def solution(values_text: str) -> int:
    values = [int(value) for value in values_text.strip("[]").split(", ")]
    include_sum = exclude_sum = 0
    for value in values:
        new_exclude_sum = max(include_sum, exclude_sum)
        include_sum = exclude_sum + value
        exclude_sum = new_exclude_sum
    return max(include_sum, exclude_sum)

if __name__=="__main__":
    parameter = input() # "[10, 12, 6, 3, 4, 10, 2]"
    print(solution(parameter)) # 26 (=10 + 6 + 10)