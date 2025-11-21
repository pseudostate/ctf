import math
from pwn import context, remote
from sage.all import PolynomialRing, Zmod
from Crypto.Util.number import long_to_bytes

def get_collision_sample_count(all_count: int, probability: float) -> int:
    '''
    collision_sample_count = ⌈√(-all_count * ln(1 - probability))⌉
    '''
    return math.ceil(math.sqrt(-all_count * math.log(1 - probability)))

def get_c(rem: remote, scramble: int) -> int:
    rem.recvuntil(b"scramble the flag: ")
    rem.sendline(str(scramble).encode())
    rem.recvuntil(b"c = ")
    return int(rem.recvline().strip().decode())

def check_franklin_reiter_related_message(e: int, n: int, c1: int, c2: int, a1: int, b1: int, a2: int, b2: int) -> int | None:
    x = PolynomialRing(Zmod(n), "x").gen()
    f1 = (a1 * x + b1) ** e - c1
    f2 = (a2 * x + b2) ** e - c2
    while f2 != 0:
        f1, f2 = f2, f1 % f2
    g = f1 # g = gcd(f1, f2)
    return int(-g.monic().constant_coefficient()) if g.degree() == 1 else None

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    all_cipher_count = 100000
    find_probability = 0.67
    sample_count = get_collision_sample_count(all_cipher_count, find_probability)
    a1 = a2 = b1 = 1
    b2 = 2
    with remote(host, port) as rem:
        rem.recvuntil(b"n, e = (")
        n = int(rem.recvuntil(b", ", drop = True).decode())
        e = int(rem.recvuntil(b")", drop = True).decode())
        c1_list = [get_c(rem, b1) for _ in range(sample_count)]
        c2_list = [get_c(rem, b2) for _ in range(sample_count)]
    for c1 in c1_list:
        for c2 in c2_list:
            m = check_franklin_reiter_related_message(e, n, c1, c2, a1, b1, a2, b2)
            if m:
                flag = long_to_bytes(m >> 256).decode()
                break
        else:
            continue
        break
    return flag

if __name__ == "__main__":
    host = "amt.rs"
    port = "33231"
    print(solution(host, port))
    