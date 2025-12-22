from pwn import context, remote
from Crypto.Util.number import isPrime, getPrime
from Crypto.PublicKey import RSA

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        for _ in range(32):
            rem.recvuntil(b"p = ")
            p = int(rem.recvline().strip().decode())
            k = 0
            while True:
                k += 1
                q = k * p + 1
                if not isPrime(q):
                    continue
                n = p * q
                e = getPrime(64)
                d = pow(e, -1, (p - 1) * (q - 1))
                try:
                    RSA.construct((n, e, d))
                except:
                    break
            rem.sendlineafter(b"q: ", str(q).encode())
        rem.recvuntil(b"SECCON")
        flag = "SECCON" + rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "yukari.seccon.games"
    port = "15809"
    print(solution(host, port))
