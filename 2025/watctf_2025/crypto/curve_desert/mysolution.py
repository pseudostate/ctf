import random, ecdsa
from Crypto.Util.number import bytes_to_long
from pwn import context, remote
curve = ecdsa.curves.BRAINPOOLP512r1
gen = curve.generator
n = curve.order

def my_sign(message: bytes, private_key: int, nonce: int) -> tuple[int, int]:
    z = bytes_to_long(message)
    rpoint = nonce * gen
    r = rpoint.x() % n
    assert r != 0
    s = (pow(nonce, -1, n) * (z + r * private_key)) % n
    return (int(r), int(s))

def sign_message(rem: remote, message: bytes) -> list[int]:
    rem.sendlineafter(b"Choose an option: ", str(1).encode())
    rem.sendlineafter(b"Input hex of message to sign: ", message.hex().encode())
    rem.recvuntil(b"Your signature is: ")
    return [int(value) for value in rem.recvline().strip().decode().split(" ")]

def calculate_private_key(message_list: list[bytes], r: int, s1: int, s2: int) -> int:
    r'''
        private_key = (s2 * z1 - s1 * z2) / (r * (s1 - s2))
        s1 = sign(message1)
        s2 = sign(message2)
        z1 = bytes_to_long(message1)
        z2 = bytes_to_long(message2)
    '''
    z1 = bytes_to_long(message_list[0])
    z2 = bytes_to_long(message_list[1])
    numerator = (s2 * z1 - s1 * z2) % n
    denominator_inverse = pow(r * (s1 - s2), -1, n)
    return (numerator * denominator_inverse) % n

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    message_list = [b"EQST", b"sk1240256"]
    with remote(host, port) as rem:
        rem.recvuntil(b"Challenge hex: ")
        challenge = rem.recvline().strip().decode()
        r, s1 = sign_message(rem, message_list[0])
        r, s2 = sign_message(rem, message_list[1]) # r is same
        private_key = calculate_private_key(message_list, r, s1, s2)
        my_k = random.randint(1, n - 1)
        my_r, my_s = my_sign(bytes.fromhex(challenge), private_key, my_k)
        rem.sendlineafter(b"Choose an option: ", str(2).encode())
        rem.sendlineafter(b"Input hex of message to verify: ", challenge.encode())
        rem.sendlineafter(b"Input the two integers of the signature seperated by a space: ", f"{my_r} {my_s}".encode())
        rem.recvline_contains(b"Message verified successfully!")
        rem.recvline_contains(b"You have passed the challenge! Your reward:")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "challs.watctf.org"
    port = "3788"
    print(solution(host, port))
    