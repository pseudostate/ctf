from pwn import context, remote
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.sendlineafter(b"Your choice: ", b"2")
        key_values = rem.recvline_contains(b"KEYS=").decode().strip().split("=")[1]
        key_list = [key.strip().replace("'", "") for key in key_values.strip("[]").split(",")]
        nonce = rem.recvline_contains(b"nonce=").strip().decode().split("=", 1)[1]
        parts = [
            b"gib m",
            b"e fla",
            b"g pli",
            b"s"
        ]
        plain = b"".join([part + b" " * (16 - len(part)) for part in parts])
        cipher = AESGCMSIV(bytes.fromhex(key_list[0])).encrypt(bytes.fromhex(nonce), plain, b"")
        rem.sendlineafter(b"Your choice: ", b"3")
        rem.sendlineafter(b"(hex): ", cipher.hex().encode())
        rem.sendlineafter(b"Your choice: ", b"4")
        rem.recvuntil(b"Here is the flag: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "remote.infoseciitr.in"
    port = "4004"
    print(solution(host, port))
    