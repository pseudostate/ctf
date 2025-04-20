def tfkysf(param_1: int, param_2: int) -> int:
    param_1 &= 0xff
    param_2 &= 0xff
    param_1_msb = (param_1 >> 7) & 1
    return param_1 >> (8 - (param_2 & 7) & 0x1f) | param_1 << (param_2 & 7)

def jistcuazjdma(param_1: int, param_2: int) -> int:
    param_1 &= 0xff
    param_2 &= 0xff
    return tfkysf(param_1 ^ param_2 * ord("%"), (param_2 + 3) % 7) + ord("*")

def b(param_1: int, param_2: int) -> int:
    param_1 &= 0xff
    param_2 &= 0xff
    return param_1 << (8 - (param_2 & 7) & 0x1f) | param_1 >> (param_2 & 7)

def evhmllcbyoqu() -> str:
    flag = ""
    memory = [
        0x32, 0xc0, 0xbf, 0x6c, 0x61, 0x85, 0x5c, 0xe4,
        0x40, 0xd0, 0x8f, 0xa2, 0xef, 0x7c, 0x4a, 0x02,
        0x04, 0x9f, 0x37, 0x18, 0x68, 0x97, 0x39, 0x33,
        0xbe, 0xf1, 0x20, 0xf1, 0x40, 0x83,
        0x06, 0x7e,
        0xf1, 0x46, 0xa6, 0x47, 0xfe, 0xc3,
        0xc8, 0x67, 0x04, 0x4d, 0xba, 0x10, 0x9b, 0x33
    ]
    for index in range(0x2e):
        for c in range(0x20, 0x7f):
            v1 = jistcuazjdma(c, index)
            v2 = b(v1 ^ 0xf, index % 8) & 0xff
            if v2 == memory[index]:
                flag += chr(c)
                break
        else:
            print("end of index :", index)
    return flag

def solution() -> str:
    return evhmllcbyoqu()

if __name__ == "__main__":
    print(solution())
    