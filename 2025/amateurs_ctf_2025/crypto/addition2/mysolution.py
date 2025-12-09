import cuso
from pwn import context, remote
from sage.all import polygens, Zmod
from Crypto.Util.number import long_to_bytes

def get_c(rem: remote, scramble: int) -> int:
    rem.recvuntil(b"scramble the flag: ")
    rem.sendline(str(scramble).encode())
    rem.recvuntil(b"c = ")
    return int(rem.recvline().strip().decode())

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    flag_length = 72
    shift_bits = 256
    with remote(host, port) as rem:
        rem.recvuntil(b"n, e = (")
        n = int(rem.recvuntil(b", ", drop = True).decode())
        e = int(rem.recvuntil(b")", drop = True).decode())

        x, y = polygens(Zmod(n), "x, y")
        f = x ** 3 - get_c(rem, 0)
        g = (x + y) ** 3 - get_c(rem, 0)

    bounds = {x: (0, 2 ** (flag_length * 8 + shift_bits)), y: (0, 2 ** shift_bits)}
    roots = cuso.find_small_roots([f, g], bounds)
    flag = long_to_bytes(roots[0][x] >> shift_bits).decode()
    return flag

if __name__ == "__main__":
    host = "amt.rs"
    port = "45195"
    print(solution(host, port))
    