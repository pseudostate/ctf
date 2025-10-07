import os, re, gmpy2
from sympy.ntheory.modular import crt
from sympy.ntheory.continued_fraction import Rational, continued_fraction_convergents, continued_fraction
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            if " = " in line:
                key, value = line.strip().split(" = ")
                if "," in value:
                    values = value.replace("[", "").replace("]", "").split(", ")
                    data[key] = [int(value, 16) if re.search("[a-fA-F]", value) else int(value) for value in values]
                else:
                    data[key] = int(value, 16) if re.search("[a-fA-F]", value) else int(value)
    return data

def wiener_attack(e: int, n: int, need_p_q: bool = False) -> tuple[int]:
    convergents = continued_fraction_convergents(continued_fraction(Rational(e, n)))
    for convergent in convergents:
        k = convergent.p # numerator
        d = convergent.q # denominator
        if k == 0 or (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        delta = s * s - 4 * n
        if delta >= 0 and gmpy2.is_square(delta):
            p = (s - int(gmpy2.isqrt(delta))) // 2
            q = (s + int(gmpy2.isqrt(delta))) // 2
            return (d, p, q) if need_p_q else (d)
    return None

def solution(file_name: str) -> str:
    data = get_data(file_name)
    e = crt(data["primes"], data["e_residues"])[0]
    n = data["N"]
    ct = data["ct"]
    d, p, q = wiener_attack(e, n, True)
    key = sha256((str(p) + str(q)).encode()).digest()
    block_size = 16
    flag = unpad(AES.new(key, AES.MODE_ECB).decrypt(long_to_bytes(ct)), block_size).decode()
    return flag

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    