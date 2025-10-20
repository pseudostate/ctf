import os, ast
from sage.all import PolynomialRing, Zmod
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from sympy import isprime

def get_data(file_name: str, delimit: str) -> dict[str, any]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            if delimit in line:
                key, value = line.strip().split(delimit)
                if value.startswith("b'") or value.startswith('b"'):
                    data[key] = ast.literal_eval(value)
                else:
                    data[key] = int(value)
    return data

def solution(file_name: str, delimit: str) -> str:
    data = get_data(file_name, delimit)
    gift = data["gift"]
    mod = data["mod"]
    c = data["c"]
    nonce = data["nonce"]

    x = PolynomialRing(Zmod(mod), names = ("x",)).gen()
    f1 = x ** 2 - x + (3 - gift)
    f2 = x ** 2 + 3 * x + (5 - gift)
    
    x_candidates = []
    for root, _ in f1.roots():
        x_candidates.append(int(root))
    for root, _ in f2.roots():
        x_candidates.append(int(root))
    for x_candidate in x_candidates:
        p_candidate = x_candidate ** 2 + x_candidate + 3
        if isprime(p_candidate):
            p = p_candidate
            break
    key = long_to_bytes(p)[:16]
    cipher = AES.new(key, AES.MODE_CTR, nonce = nonce)
    return cipher.decrypt(c).decode()

if __name__ == "__main__":
    file_name = "output.txt"
    delimit = " = "
    print(solution(file_name, delimit))
