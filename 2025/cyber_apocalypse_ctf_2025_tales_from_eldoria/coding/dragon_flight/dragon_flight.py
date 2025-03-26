# 1차원 리스트에서 구간 최대 부분합(Q) 출력과 데이터 업데이트(U) 진행
def solution(array: list[int], start_index: int, end_index: int) -> int:
    max_sum = -pow(2, 31)
    current_sum = 0
    for index in range(start_index - 1, end_index):
        current_sum += array[index]
        max_sum = max(max_sum, current_sum)
        if current_sum < 0:
            current_sum = 0
    return max_sum

if __name__=="__main__":
    parameter1, parameter2 = input().split() # "8 4"
    parameter3 = [int(value) for value in input().split()] # "-1 -5 -8 -2 -7 4 -4 -2"
    '''
    U 5 0
    U 2 -7
    U 7 8 
    Q 3 8 -> 12
    '''
    for case in range(int(parameter2)):
        query = input()
        operator, operand1, operand2 = query.split()
        if operator == "Q":
            print(solution(parameter3, int(operand1), int(operand2)))
        elif operator == "U":
            parameter3[int(operand1) - 1] = int(operand2)