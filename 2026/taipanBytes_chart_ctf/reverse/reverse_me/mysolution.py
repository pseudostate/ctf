import re
from pwn import read

def get_flag(data: bytes, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}".encode(), data)), b"").decode()

def solution(file_name: str, prefix: str) -> str:
    return get_flag(read(file_name), prefix)

if __name__ == "__main__":
    file_name = "secret.tb"
    prefix = "TB"
    print(solution(file_name, prefix))
