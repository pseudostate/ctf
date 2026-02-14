import os
from pwn import context, remote
from Crypto.Util.number import long_to_bytes

def proof_of_work_solution(rem: remote) -> None:
    rem.recvuntil(b"proof of work:\n")
    solution = os.popen(rem.recvline().strip().decode()).read().strip()
    rem.sendlineafter(b"solution: ", solution.encode())

def get_p_q(n: int) -> tuple[int, int]:
    stack = [(1, 7, 7)] # index, current_p, current_q
    possible_digits = [6, 7]    
    while stack:
        index, curr_p, curr_q = stack.pop()
        if index == 256:
            if curr_p * curr_q == n:
                return curr_p, curr_q
            continue
        for dp in possible_digits:
            for dq in possible_digits:
                next_p = dp * (10 ** index) + curr_p
                next_q = dq * (10 ** index) + curr_q
                if (next_p * next_q) % (10 ** (index + 1)) == n % (10 ** (index + 1)):
                    stack.append((index + 1, next_p, next_q))
    return None, None

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    e = 65537
    with remote(host, port) as rem:
        proof_of_work_solution(rem)
        rem.recvuntil(b"n=")
        n = int(rem.recvline().strip().decode())
        rem.recvuntil(b"c=")
        c = int(rem.recvline().strip().decode())
    p, q = get_p_q(n)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    flag = long_to_bytes(m).decode()
    return flag

if __name__ == "__main__":
    host = "chall.lac.tf"
    port = "31180"
    print(solution(host, port))
    