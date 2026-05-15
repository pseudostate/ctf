import os, requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(reference_file: str, prefix: str) -> str:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), reference_file), "rb") as f:
        flag = get_flag(f.read().decode("latin-1"), prefix)
    return flag

if __name__ == "__main__":
    reference_file = "riscal"
    prefix = "midnight"
    print(solution(reference_file, prefix))
