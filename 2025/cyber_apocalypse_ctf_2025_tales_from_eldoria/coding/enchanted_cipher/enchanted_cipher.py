# (알파벳이 아닌 문자는 무시하고) 주어진 알파벳을 5개씩 그룹으로 묶어서 시프트 복호화
def solution(ciphers_text: str, shift_group_count: int, shift_group_text: str) -> str:
    answer = ""
    shift_group = [int(value) for value in shift_group_text.strip("[]").split(", ")]
    index = 0
    for c in ciphers_text:
        if "a" <= c <= "z":
            answer += chr(((ord(c) - ord("a") - shift_group[index // 5] + 26) % 26) + ord("a"))
            index += 1
        else:
            answer += c
            continue
    return answer

if __name__=="__main__":
    parameter1 = input() # "fjmoo suneu eccq gzehnx"
    parameter2 = input() # "4"
    parameter3 = input() # "[8, 3, 16, 14, 9]"
    print(solution(parameter1, int(parameter2), parameter3)) # "xbegg prkbr omma qlqtzj"