def solution(key: str, output: bytes) -> str:
    flag = ""
    carry = 0
    for index, out in enumerate(bytes.fromhex(output.decode())):
        val = out ^ ord(key[index % len(key)])
        val -= carry
        while val < 0:
            val += 0x100
        flag += chr(val)
        carry += val
        carry %= 0x100
    return flag

if __name__ == "__main__":
    key = "Awesome!"
    output = b"23a326c27bee9b40885df97007aa4dbe410e93"
    print(solution(key, output))
    