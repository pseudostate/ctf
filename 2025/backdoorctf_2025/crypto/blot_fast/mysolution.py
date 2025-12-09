import os, math
from sage.all import GCD, primes
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str, delimit: str) -> dict[str, any]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            if delimit in line:
                key, value = line.strip().split(delimit)
                data[key] = int(value)
    return data

def solution(file_name: str, delimit: str) -> str:
    r'''
    2 ** 15 < dp_smart < 2 ** 16
    e * dp_smart ≡ 1 (mod p-1)
    e * dp_smart = k * (p-1) + 1
    Fermat's Little Theorem (a ⊥ p): a ** (p-1) ≡ 1 (mod p)
    a ** (e * dp_smart - 1) ≡ a ** (k * (p-1)) ≡ (a ** (p - 1)) ** k ≡ 1 ** k ≡ 1 (mod p)
    ∴ a ** (e * dp_smart - 1) - 1 ≡ 0 (mod p)
    p | (a ** (e * dp_smart - 1) - 1)
    ∴ p = GCD(a ** (e * dp_smart - 1) - 1, N)
    '''
    data = get_data(file_name, delimit)
    n = data["N"]
    e = data["e"]
    c = data["c"]
    for dp_smart_candidate in primes(2 ** 15, 2 ** 16):
        p_candidate = GCD(pow(2, e * dp_smart_candidate - 1, n) - 1, n)
        if 1 < p_candidate < n:
            p = p_candidate
            q = n // p
            phi = (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            m = pow(c, d, n)
            flag = long_to_bytes(m).decode()
            break
    return flag

if __name__ == "__main__":
    file_name = "output.txt"
    delimit = " = "
    print(solution(file_name, delimit))
