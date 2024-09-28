def solution(pt1: str, ct1: str, ct2: str) -> str:
    answer = bytearray()
    for pt1_byte, ct1_byte, ct2_byte in zip(pt1,  bytes.fromhex(ct1),  bytes.fromhex(ct2)):
        key_byte = (((1 << 8) - 1) - ct1_byte) ^ pt1_byte
        answer_byte = (((1 << 8) - 1) - ct2_byte) ^ key_byte
        answer.append(answer_byte)
    return answer.decode('utf-8')

if __name__ == "__main__":
    pt1 = b"Blue is greener than purple for sure!"
    ct1 = "fe9d88f3d675d0c90d95468212b79e929efffcf281d04f0cfa6d07704118943da2af36b9f8"
    ct2 = "de9289f08d6bcb90359f4dd70e8d95829fc8ffaf90ce5d21f96e3d635f148a68e4eb32efa4"
    print(solution(pt1, ct1, ct2))
    