import re
from pwn import context, remote
from Crypto.Util.number import long_to_bytes

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.recvuntil(b"N = ")
        n = int(rem.recvline().strip().decode())
        rem.recvuntil(b"e = ")
        e = int(rem.recvline().strip().decode())
        rem.recvuntil(b"x0: ")
        x0 = int(rem.recvline().strip().decode())
        rem.recvuntil(b"x1: ")
        x1 = int(rem.recvline().strip().decode())

        # v = (x0 + (int(k) ⊕ e)) % n
        # x0 + (k ⊕ e) ≡ x1 (mod n)
        # k ⊕ e ≡ x1 - x0 (mod n)
        # k ≡ e ⊕ (x1 - x0) (mod n)

        k = e ^ ((x1 - x0) % n)
        rem.sendlineafter(b"Please pick a value k.\n", str(k).encode())

        rem.recvuntil(b"Message 1:  ")
        m0 = int(rem.recvline().strip().decode())
        rem.recvuntil(b"Message 2:  ")
        m1 = int(rem.recvline().strip().decode())
        try:
            flag = long_to_bytes(m0).strip().decode()
        except: 
            flag = long_to_bytes(m1).strip().decode()
    return flag

if __name__ == "__main__":
    host = "challenge.utctf.live"
    port = "8379"
    print(solution(host, port))
    