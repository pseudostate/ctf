def solution(data1: list[int], data2: list[int]) -> str:
    flag = ""
    for d1, d2 in zip(data1, data2):
        flag += chr(d1 ^ d2)
    return flag

if __name__ == "__main__":
    DAT_00402000 = [
        0x20, 0x22, 0x20, 0x26, 0x35, 0x37, 0x14, 0x07,
        0x46, 0x00, 0x5a, 0x17, 0x44, 0x35, 0x52, 0x0c,
        0x70, 0x28, 0x37, 0x1c, 0x5b, 0x1d, 0x70, 0x16,
        0x76, 0x50, 0x69, 0x5c, 0x6e, 0x6c, 0x1b, 0x12,
        0x54, 0x69, 0x2d, 0x38, 0x06, 0x23, 0x11, 0x3d,
        0x2f, 0x00, 0x02, 0x4a, 0x68, 0x45, 0x3b, 0x64,
        0x1a, 0x20, 0x55, 0x05
    ]
    DAT_00402034 = [
        0x75, 0x6f, 0x64, 0x65, 0x61, 0x71, 0x6f, 0x75,
        0x75, 0x76, 0x69, 0x45, 0x60, 0x70, 0x7f, 0x65,
        0x54, 0x77, 0x63, 0x74, 0x68, 0x42, 0x53, 0x54,
        0x45, 0x03, 0x3d, 0x7f, 0x31, 0x58, 0x75, 0x46,
        0x75, 0x44, 0x60, 0x78, 0x6a, 0x74, 0x51, 0x4f,
        0x1c, 0x5f, 0x76, 0x79, 0x0b, 0x2d, 0x75, 0x45,
        0x4b, 0x55, 0x66, 0x78
    ]
    print(solution(DAT_00402000, DAT_00402034))
    