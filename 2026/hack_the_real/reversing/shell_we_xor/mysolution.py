import os, re
from Crypto.Util.number import long_to_bytes, bytes_to_long

def get_data(reference_file: str) -> bytes:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), reference_file), "rb") as f:
        data = f.read()
    return data

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def read_qword(data: bytearray, offset: int) -> int:
    return bytes_to_long(bytes(reversed(data[offset : offset + 8])))

def write_qword(data: bytearray, offset: int, value: int) -> None:
    data[offset : offset + 8] = bytes(reversed(long_to_bytes(value, 8)))

def solution(reference_file: str, prefix: str) -> str:
    data = bytearray(get_data(reference_file))
    constant = 0x0df0adbaefbeadde
    for i in range(63):
        offset = 5 + i * 8
        write_qword(data, offset, read_qword(data, offset) ^ read_qword(data, 5) ^ constant)
    for i in range(34):
        offset = 0x2d7 + i * 8
        write_qword(data, offset, read_qword(data, offset) ^ constant)
    flag = get_flag(data.decode("latin-1"), prefix)
    return flag

if __name__ == "__main__":
    reference_file = "sc.bin"
    prefix = "EQST"
    print(solution(reference_file, prefix))