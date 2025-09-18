import os
from Crypto.Util.number import long_to_bytes
from sympy import prevprime
from gmpy2 import iroot

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
    n = data["N"]
    e = data["e"]
    ct = data["ct"]
    p = iroot(n // 2, 2)[0]
    while n % p != 0:
        p = prevprime(p)
    phi = (p - 1) * (n // p - 1)
    d = pow(e, -1, phi)
    pt = pow(ct, d, n)
    flag = long_to_bytes(pt).decode()
    return flag

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    