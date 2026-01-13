import base64, string
from pwn import context, remote
from collections import Counter

def query(rem, idx: int, u: bytes) -> bytes:
    rem.sendlineafter(b"> ", f"{idx}:{u.hex()}".encode())
    out = rem.recvline().strip()
    try:
        return base64.b64decode(out)
    except:
        return b""

def get_filler_length_and_encrypt_reference_block(rem: remote, block_size: int, m: int, n: int) -> list[tuple[int, bytes]]:
    filler_length_and_encrypt_reference_block = []
    max_reference_block_count = (m - block_size) // block_size
    for filler_length in range(block_size): # (self.pl + filler_byte * filler_length) % block_size == 0
        blocks = []
        u = b"F" * filler_length + b"R" * block_size * max_reference_block_count
        for idx in range(n):
            blocks.append(query(rem, idx, u))
        most_appear_block, frequency = Counter(blocks).most_common(1)[0]
        if frequency == max_reference_block_count:
            filler_length_and_encrypt_reference_block.append((filler_length, most_appear_block))
    return filler_length_and_encrypt_reference_block

def get_append_q_indexes(rem: remote, block_size: int, m: int, n: int, filler_length: int, encrypted_reference_block: bytes) -> list[int]:
    max_filler_append_index = (m - block_size - filler_length) // block_size
    append_q_indexes = [-1] * (max_filler_append_index + 1)
    for filler_append_index in range(max_filler_append_index + 1):
        u = b"F" * filler_length + b"D" * block_size * filler_append_index + b"R" * block_size
        for q_out_index in range(n):
            encrypt_block = query(rem, q_out_index, u)
            if encrypt_block == encrypted_reference_block:
                append_q_indexes[filler_append_index] = q_out_index
    return append_q_indexes

def get_flag(rem: remote, block_size: int, filler_length: int, append_q_indexes: list[int]) -> str:
    flag = ""
    while not flag.endswith("}"):
        dummy_length = block_size - 1 - (len(flag) % block_size)
        dummy_filler_append_index = (dummy_length + len(flag)) // block_size
        real_q_index = append_q_indexes[dummy_filler_append_index]
        prefix = b"F" * filler_length + b"D" * dummy_length
        target_block = query(rem, real_q_index, prefix) # previous 15 bytes + flag[current_flag_index]
        for c in string.printable:
            guess_byte = c.encode()
            result_block = query(rem, real_q_index, prefix + flag.encode() + guess_byte) # previous 15 bytes + output(encrypt(guess))
            if result_block == target_block:
                flag += c
                break
    return flag

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    block_size = 16
    m = 256
    l = 1024
    n = l // block_size + 1 # 65
    with remote(host, port) as rem:
        filler_length_and_encrypt_reference_block = get_filler_length_and_encrypt_reference_block(rem, block_size, m, n)
        while len(filler_length_and_encrypt_reference_block) > 1: # collision check
            filler_length_and_encrypt_reference_block = get_filler_length_and_encrypt_reference_block(rem, block_size, m, n)
        filler_length, encrypt_reference_block = filler_length_and_encrypt_reference_block[0]
        append_q_indexes = get_append_q_indexes(rem, block_size, m, n, filler_length, encrypt_reference_block)
        flag = get_flag(rem, block_size, filler_length, append_q_indexes)
    return flag

if __name__ == "__main__":
    host = "34.186.247.84"
    port = "5000"
    print(solution(host, port))
    