import os
from pwn import context, remote
from sage.all import euler_phi

def proof_of_work_solution(rem: remote) -> None:
    rem.recvuntil(b"proof of work:\n")
    solution = os.popen(rem.recvline().strip().decode()).read().strip()
    rem.sendlineafter(b"solution: ", solution.encode())

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        proof_of_work_solution(rem)
        rem.recvuntil(b"n = ")
        n = int(rem.recvline().strip().decode())
        rem.recvuntil(b"e = ")
        e = int(rem.recvline().strip().decode())
        rem.recvuntil(b"c = ")
        c = int(rem.recvline().strip().decode())
        phi = euler_phi(n) # phi(p ** a * q ** b) = (p ** a - p ** (a - 1)) * (q ** b - q ** (b - 1))
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        rem.sendlineafter(b"How many treats do I want? ", str(m).encode())
        rem.recvuntil(b"Here's your reward, human:\n")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "chall.lac.tf"
    port = "31225"
    print(solution(host, port))
    