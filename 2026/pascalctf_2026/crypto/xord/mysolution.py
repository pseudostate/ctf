import os, random
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str) -> int:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        return int(f.read(), 16)

def solution(file_name: str) -> str:
    flag_bytes = []
    c = get_data(file_name)
    random.seed(1337)
    for b in long_to_bytes(c):
        random_key = random.randint(0, 255)
        flag_bytes.append(b ^ random_key)
    return bytes(flag_bytes).decode()

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
