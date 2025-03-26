# 2차원 리스트에서 각 1차원 리스트의 숫자를 하나씩 선택하여 합이 target과 같은 조합 계산
def backtracking(answer: list[int], index: int, current_sum: int, T: int, array: list[list[int]]) -> list[int]:
    result = None
    if index == len(array) and current_sum == T:
        result = answer
    elif index < len(array):
        for value in array[index]:
            result = backtracking(answer + [value], index + 1, current_sum + value, T, array)
            if result:
                break
    return result

def solution(array_text: str, T: int) -> int:
    array_text = array_text.strip("[]").split("], [")
    array = []
    for subarray_text in array_text:
        array.append([int(value) for value in subarray_text.strip("[]").split(", ")])
    return backtracking([], 0, 0, T, array)

if __name__=="__main__":
    parameter1 = input() # "[[5, 7, 21], [8, 26, 24, 26], [28, 9], [17, 8], [22, 29]]"
    parameter2 = input() # "82"
    print(solution(parameter1, int(parameter2))) # "[7, 8, 28, 17, 22]"