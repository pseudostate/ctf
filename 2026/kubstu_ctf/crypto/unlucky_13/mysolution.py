import hashlib, os, re
from Crypto.Cipher import ARC4
from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot
from pwn import xor

def get_data(reference_file: str, delimit: str) -> dict:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), reference_file), "r") as f:
        for line in f:
            if delimit in line:
                key, value = line.strip().split(delimit)
                data[key] = int(value)
    return data

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def cursed_prng(seed: int, length: int) -> bytes:
    state = seed
    stream = []
    for _ in range(length):
        state = (state * 1313 + 131313) % (2**32)
        stream.append(state & 0xFF)
    return bytes(stream)

def solution(reference_file: str, delimit: str, prefix: str) -> str:
    UNLUCKY_NUMBER = 13
    secret = b"Unlucky" + str(UNLUCKY_NUMBER).encode()
    key = hashlib.sha256(secret).digest()[:16]
    
    c = get_data(reference_file, delimit)["c"]
    m, _ = iroot(c, 3)
    layer2 = long_to_bytes(int(m))
    layer1 = ARC4.new(key).decrypt(layer2)
    flag = xor(layer1, cursed_prng(UNLUCKY_NUMBER, len(layer1))).decode()
    return get_flag(flag, prefix)

if __name__ == "__main__":
    reference_file = "output.txt"
    delimit = " = "
    prefix = "KubSTU"
    print(solution(reference_file, delimit, prefix))
