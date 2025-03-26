import base64

def solution(hex_value: int) -> int:
    decode_value = base64.b64decode(bytes.fromhex(hex(hex_value)[2:])).decode()
    return decode_value[::-1]

if __name__=="__main__":
    hex_value = 0x656d46795a6d5a31626b64735a574657
    print(solution(hex_value))
