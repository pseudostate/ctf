def solution(data_list: list[str]) -> str:
    return "".join(map(chr, [c - 1 for c in data_list]))

if __name__=="__main__":
    data_list = [118, 115, 100, 105, 106, 111, 116, 102, 100, 124, 66, 84, 68, 74, 74, 96, 117, 115, 53, 111, 116, 103, 49, 115, 110, 96, 50, 99, 105, 57, 102, 54, 126]
    print(solution(data_list))
