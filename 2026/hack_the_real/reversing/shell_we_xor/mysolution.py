import re, struct

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(reference_file: str, prefix: str) -> str:
    data = bytearray(open(reference_file, "rb").read())

    enc_qword = struct.unpack_from("<Q", data, 5)[0]
    key1 = enc_qword ^ 0x0df0adbaefbeadde
    for i in range(63):
        offset = 5 + i * 8
        qw = struct.unpack_from("<Q", data, offset)[0]
        struct.pack_into("<Q", data, offset, qw ^ key1)

    key2 = 0x0df0adbaefbeadde
    for i in range(34):
        offset = 0x2d7 + i * 8
        qw = struct.unpack_from("<Q", data, offset)[0]
        struct.pack_into("<Q", data, offset, qw ^ key2)

    flag = get_flag(data.decode(errors = "ignore"), prefix)
    return flag

if __name__ == "__main__":
    reference_file = "sc.bin"
    prefix = "EQST"
    print(solution(reference_file, prefix))