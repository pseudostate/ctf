def decrypt_twin_hex(twin_hex_sentence: str) -> str:
    base36 = [chr(a) + chr(b) for a in range(32, 128) for b in range(32, 128)]
    return "".join(base36[int(twin_hex, 36)] for twin_hex in [twin_hex_sentence[i:i+3] for i in range(0, len(twin_hex_sentence), 3)] if twin_hex.strip())

def solution(file_name: str) -> str:
    answer = ""
    with open(file_name, "r") as f:
        data = "".join(line.strip() for line in f.readlines())
        data = data.replace(",", " ").replace(";", " ").replace(":", " ").replace("%", " ").replace("\\x", " ").replace("0x", " ").split()
        decode_text = ""
        for value in data:
            if len(value) == 2:
                decode_text += chr(int(value, 16))
            elif len(value) == 4:
                decode_text += chr(int(value[:2], 16))
                decode_text += chr(int(value[2:], 16))
            elif len(value) > 4:
                decode_text += chr(int(value[:2], 16))
                decode_text += decrypt_twin_hex(value[2:])
        print(decode_text)
    return answer

if __name__=="__main__":
    file_name = "chall.txt"
    print(solution(file_name))
