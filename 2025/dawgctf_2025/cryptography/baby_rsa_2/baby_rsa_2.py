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
    e_pub, d_pub, n, c = data["e"], data["d"], data["N"], data["c"]
    e_priv = 0x10001
    # e * d ≡ 1 (mod phi)
    d_priv = pow(e_priv, -1, e_pub * d_pub - 1)
    m = pow(c, d_priv, n)
    return long_to_bytes(m).decode()

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    