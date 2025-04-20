import os
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            if " = " in line:
                key, value = line.strip().split(" = ")
                data[key] = int(value)
    return data

def solution(file_name: str) -> str:
    data = get_data(file_name)
    n, e, ct = data["N"], data["e"], data["ct"]
    a, b, c, d, x, y = data["a"], data["b"], data["c"], data["d"], data["x"], data["y"]
    # x = ap + bq, y = cp + dq
    p = (d * x - b * y) // (a * d - b * c) # p = (dx - by) / (ad - bc)
    q = (a * y - c * x) // (a * d - b * c) # q = (ay - cx) / (ad - bc)
    phi = (p - 1) * (q - 1)
    decrypt_key = pow(e, -1, phi)
    m = pow(ct, decrypt_key, n)
    return long_to_bytes(m).decode()

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    