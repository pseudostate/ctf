from pwn import context, remote
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

def adjust_key(key8: bytes) -> bytes:
    out = bytearray()
    for b in key8:
        b7 = b & 0xFE                
        ones = bin(b7).count("1")     
        out.append(b7 | (ones % 2 == 0))  
    return bytes(out)

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})

    block_size = 8
    normal_k2 = "0202020202020202"
    normal_k3 = "0101010101010101"
    weak_k2 = "011f011f010e010e"
    weak_k3 = "1f011f010e010e01"

    with remote(host, port) as rem:
        rem.sendlineafter(b"enter k2 hex bytes >", normal_k2.encode())
        rem.sendlineafter(b"enter k3 hex bytes >", normal_k3.encode())
        rem.sendlineafter(b"enter option >", b"1")
        rem.sendlineafter(b"enter option >", b"1")
        rem.recvuntil(b"ciphertext : ")
        cipher_flag = rem.recvline().strip().decode()

        rem.sendlineafter(b"enter k2 hex bytes >", weak_k2.encode())
        rem.sendlineafter(b"enter k3 hex bytes >", weak_k3.encode())
        rem.sendlineafter(b"enter option >", b"3")
        rem.sendlineafter(b"enter option >", b"2")
        rem.sendlineafter(b"enter hex bytes >", cipher_flag.encode())
        rem.recvuntil(b"ciphertext : ")
        weak_cipher_flag = rem.recvline().strip().decode()
        rem.close()
    
    unpad_weak_cipher_flag = bytes.fromhex(weak_cipher_flag)[:len(bytes.fromhex(cipher_flag))]
    cipher2 = DES.new(adjust_key(bytes.fromhex(normal_k2)), DES.MODE_ECB)
    cipher3 = DES.new(adjust_key(bytes.fromhex(normal_k3)), DES.MODE_ECB)
    flag = unpad(cipher3.decrypt(cipher2.encrypt(unpad_weak_cipher_flag)), block_size).decode()
    return flag

if __name__ == "__main__":
    host = "20.193.149.152"
    port = "1340"
    print(solution(host, port))
    