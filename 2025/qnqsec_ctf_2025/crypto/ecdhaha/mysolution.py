import sys, re, json, hashlib
from sage.all import GF, EllipticCurve, ZZ, factor
from pwn import context, remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def connect(host: str, port: str, public_x: int) -> tuple[tuple[int, int], bytes, bytes]:
    with remote(host, port) as rem:
        rem.sendlineafter(b"[mitm] A: ", str(public_x).encode())
        rem.recvuntil(b"[mitm] B': ")
        xy = rem.recvline().strip().decode()
        match = re.search(r"\((\d+), (\d+)\)", xy)
        point = (int(match.group(1))), (int(match.group(2)))
        data = json.loads(rem.recvline().strip().decode())
        iv = bytes.fromhex(data["iv"])
        ct = bytes.fromhex(data["ct"])
    return point, iv, ct

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    p = 0xffffffffffffffffffffffffffffffffffffffffffffff13
    F = GF(p)

    points = []
    while len(points) < 2:
        point, _, _ = connect(host, port, 0)
        x, y = F(point[0]), F(point[1])
        if not points or x != points[0][0]:
            points.append((x, y))

    (x1, y1), (x2, y2) = points[0], points[1]
    a = ((y1 ** 2 - x1 ** 3) - (y2 ** 2 - x2 ** 3)) / (x1 - x2)
    b = (y1 ** 2 - x1 ** 3) - a * x1

    EC = EllipticCurve(F, [a, b])
    G_rand = EC.random_point() 
    q = EC.order()

    d = -1
    for f, _ in factor(q):
        if f < 10000:
            d = int(f)
            break
    
    P = (q // d) * G_rand
    if P.is_zero():
        P = (q // d) * EC.random_point()
    _, iv, ct = connect(host, port, int(ZZ(P.x())))

    for i in range(d):
        R_guess = i * P
        if R_guess.is_zero():
            continue
        secret_guess = int(R_guess.x())
        key_guess = hashlib.sha256(str(secret_guess).encode()).digest()[:16]
        try:
            cipher = AES.new(key_guess, AES.MODE_CBC, iv = iv)
            flag = unpad(cipher.decrypt(ct), 16).decode()
            break
        except:
            continue
    return flag

if __name__ == "__main__":
    host = "te4.uk"
    port = "1337"
    print(solution(host, port))
