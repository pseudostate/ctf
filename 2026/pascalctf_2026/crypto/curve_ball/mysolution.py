from pwn import context, remote
from sage.all import EllipticCurve, GF

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    p = 1844669347765474229
    a = 0
    b = 1
    n = 1844669347765474230
    Gx = 27
    Gy = 728430165157041631
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    G = E(Gx, Gy)
    with remote(host, port) as rem:
        rem.recvuntil(b"Q = (")
        Qx = int(rem.recvuntil(b", ", drop = True).strip().decode())
        Qy = int(rem.recvuntil(b")", drop = True).strip().decode())
        Q = E(Qx, Qy)
        rem.sendlineafter(b"> ", b"1")
        rem.sendlineafter(b"secret (hex):", hex(Q.log(G)).encode())
        rem.recvuntil(b"Flag: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "curve.ctf.pascalctf.it"
    port = "5004"
    print(solution(host, port))
    