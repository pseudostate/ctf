import os
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import GF, Matrix, vector

def get_cipher_data(cipher_file: str) -> int:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), cipher_file), "rb") as f:
        data = bytes_to_long(f.read())
    return data

def get_keystream_leak(keystream_leak_file: str) -> list[int]:
    data = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), keystream_leak_file), "rb") as f:
        for line in f.readlines():
            data.append(int(line))
    return data

def int_to_vec(n: int) -> vector:
    return vector(GF(2), 32, [(n >> i) & 1 for i in range(32)])

def vec_to_int(v: vector) -> int:
    res = 0
    for i, bit in enumerate(v):
        if bit == 1:
            res |= (1 << i)
    return res

def solution(cipher_file: str, keystream_leak_file: str) -> str:
    '''
    S[n+1] = A * S[n] XOR B over GF(2)
    -> S[n+1] ≡ A * S[n] + B (mod 2)
    S[n+1] ≡ A * S[n] + B (mod 2)
    S[n+2] ≡ A * S[n+1] + B (mod 2)
    S[n+1] + S[n+2] ≡ A * (S[n] + S[n+1]) + 2 * B (mod 2) ... 2 * x ≡ 0 (mod 2)
    S[n+1] + S[n+2] ≡ A * (S[n] + S[n+1]) (mod 2)
    y = S[n+1] + S[n+2]
    x = S[n] + S[n+1]
    y ≡ A * x (mod 2)
    A ≡ y * (x ** -1) (mod 2)
    B ≡ S[1] - A * S[0] (mod 2)
    '''
    cipher_data = get_cipher_data(cipher_file)
    keystream_leak = get_keystream_leak(keystream_leak_file)
    
    states = [int_to_vec(s) for s in keystream_leak]
    deltas = [states[i] + states[i + 1] for i in range(len(states) - 1)]
    
    x = Matrix(GF(2), deltas[:-1]).transpose()
    y = Matrix(GF(2), deltas[1:]).transpose()

    A = x.transpose().solve_right(y.transpose()).transpose()
    B = states[1] - A * states[0]

    current_state_vector = states[0]
    plain = []
    for byte in long_to_bytes(cipher_data):
        plain.append(byte ^ vec_to_int(current_state_vector) & 0xFF)
        current_state_vector = A * current_state_vector + B
    flag = bytes(plain).decode()
    return flag

if __name__ == "__main__":
    cipher_file = "cipher.txt"
    keystream_leak_file = "keystream_leak.txt"
    print(solution(cipher_file, keystream_leak_file))
    