import os, json, gmpy2
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        data = json.loads(f.read())
    return data

def solution(file_name: str) -> str:
    data = get_data(file_name)
    e = int(data["e"])
    c = int(data["c"])
    pt = gmpy2.iroot(c, e)[0]
    return long_to_bytes(pt).decode()

if __name__ == "__main__":
    file_name = "challenge.txt"
    print(solution(file_name))
    