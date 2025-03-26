def solution(hex_values: list[int]) -> int:
    flag = bytearray()
    for hex_value in hex_values:
        bytes_value = hex_value.to_bytes((hex_value.bit_length() + 7) // 8, "little")
        for byte in bytes_value:
            flag.append(byte - 1)
    return flag.decode()

if __name__=="__main__":
    hex_values = [0x716e32747c435549, 0x6760346d, 0x6068356d, 0x75327335, 0x7e643275346e69]
    print(solution(hex_values))
