from pwn import *

def get_data(r: remote, name: str) -> int:
    r.recvuntil(f"{name} = ".encode())
    return int(r.recvline().decode().strip())

def solution(host: str, port: str) -> str:
    CUSTOM_PT2 = 31
    context.update({"log_level":"error"})
    r = remote(host, port)
    n = get_data(r, "n")
    e = get_data(r, "e")
    ct1 = get_data(r, "ct")
    ct3 = (ct1 * (CUSTOM_PT2 ** e)) % n
    r.sendlineafter(b'Ciphertext (int): ', str(ct3).encode())
    r.recvuntil(b"Oracle Response: Well, here is the answer that you seek : ")
    pt3 = int(r.recvline().decode().strip())
    pt1 = (pt3 // CUSTOM_PT2) % n
    return pt1.to_bytes((pt1.bit_length() + 7) // 8, "big").decode()

if __name__ == "__main__":
    host = "chals.bitskrieg.in"
    port = "7000"
    print(solution(host, port))
    