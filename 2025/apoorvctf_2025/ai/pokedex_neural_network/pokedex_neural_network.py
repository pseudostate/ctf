from pwn import *

def solution(host: str, port: str) -> str:
    flag = ""
    context.update({"arch":"i386","log_level":"error"})
    with remote(host, port) as r:
        r = remote(host, port)
        r.recvuntil(b"Question 1/4: What is the seed for the given pytorch code?")
        r.sendline(b"6") # It's the pokemon number for charizard.
        r.recvuntil(b"Question 2/4: What's the number of input features of the first linear layer?")
        r.sendline(b"10368") # 9 * 9 * 128
        r.recvuntil(b"Question 3/4: Find the sum of values in the weights of the first row in the first linear layer.")
        r.recvuntil(b"(This answer should be a decimal number with 4 decimal places X.XXXX!)")
        r.sendline(b"-3.6320") # sum(dict(pk.named_parameters())["fc1.weight"][0])
        r.recvuntil(b"Question 4/4: Enter the value of the weight matrix of the second linear layer, 3rd row 16th column.")
        r.recvuntil(b"(This answer should be a decimal number with 4 decimal places X.XXXX!)")
        r.sendline(b"-0.0241") # dict(pk.named_parameters())["fc2.weight"][2][15]
        r.recvuntil(b"Here's your reward: ")
        flag = r.recvall().decode().strip()
    return flag

if __name__ == "__main__":
    host = "chals2.apoorvctf.xyz"
    port = "4000"
    print(solution(host, port))
    