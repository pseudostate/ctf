from pwn import *
from Crypto.Cipher import ARC4

def solution(host: str, port: str) -> str:
    flag = ""
    answers = [
        "0x402db6", # Question 1: What is the address of the main function in hex (i.e. 0x1234)?
        "strlen", # Question 2: What is the name of the libc function that has the same effect as function a?
        "15", # Question 3: What is the length of the correct password?
        "0xc1de1494171d9e2f", # Question 4: Function b returns a constant value that is later used to check the password. What is the value returned by the function?
        "rc4", # Question 5: Function c implements a popular encryption algorithm. What is this algorithm?
    ]
    context.update({"arch":"amd64","log_level":"error"})
    with remote(host, port) as rem:
        for answer in answers:
            rem.recvuntil(b"Answer: ")
            rem.sendline(answer.encode())
        # Question 6: Finally, what is the correct password for this program?
        rem.recvuntil(b"Answer: ")
        enc = "0xd158158aeeb5bb520c6ba4ab6d7db7"
        key = answers[3]
        rem.sendline(ARC4.new(bytes.fromhex(key[2:])[::-1]).decrypt(bytes.fromhex(enc[2:]))) # little-endian = [::-1]
        rem.recvuntil(b"grey{")
        flag = rem.recvline().decode().strip()
    return "grey{" + flag

if __name__ == "__main__":
    host = "challs.nusgreyhats.org"
    port = "33000"
    print(solution(host, port))
    