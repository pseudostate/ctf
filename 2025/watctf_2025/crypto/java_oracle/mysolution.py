import re
from pwn import context, remote
from tqdm import trange

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def check_valid_padding(rem: remote, data: bytes, until_text: str, valid_text: str) -> bool:
    rem.recvuntil(until_text.encode())
    rem.sendline(data)
    return valid_text in rem.recvline().strip().decode()

def get_modified_prev_ct_block(byte_index: int, guess_byte: int, curr_dt_block: list[int], block_size: int = 16, default_byte_value: int = 0, check: bool = False) -> list[int]:
    padding = [guess_byte] + [curr_dt_byte ^ byte_index for curr_dt_byte in curr_dt_block[block_size - byte_index + 1:]]
    modified_prev_ct_block = [default_byte_value] * (block_size - len(padding)) + padding
    if check:
        another_byte_value = 0xFF - default_byte_value
        modified_prev_ct_block = [default_byte_value] * (block_size - len(padding) - 1) + [another_byte_value] + padding
    return modified_prev_ct_block

def get_plain_text_block(rem: remote, prev_ct_block: bytes, curr_ct_block: bytes, until_text: str, valid_text: str, block_size: int = 16, default_byte_value: int = 0) -> bytes:
    curr_dt_block = [default_byte_value] * block_size # intermediate state
    for byte_index in range(1, block_size + 1):
        valid_guess_list = []
        for guess_byte in range(0x100):
            modified_prev_ct_block = get_modified_prev_ct_block(byte_index, guess_byte, curr_dt_block, block_size, default_byte_value, False)
            if check_valid_padding(rem, (bytes(modified_prev_ct_block) + curr_ct_block).hex().encode(), until_text, valid_text):
                valid_guess_list.append(guess_byte)
        valid_correct_byte = None
        if len(valid_guess_list) == 1:
            valid_correct_byte = valid_guess_list[0]
        elif len(valid_guess_list) > 1 and byte_index < block_size: # low probability = (1 / 256) and byte_index 16 impossible
            for valid_guess_byte in valid_guess_list:
                modified_prev_ct_block = get_modified_prev_ct_block(byte_index, valid_guess_byte, curr_dt_block, block_size, default_byte_value, True)
                if check_valid_padding(rem, (bytes(modified_prev_ct_block) + curr_ct_block).hex().encode(), until_text, valid_text):
                    valid_correct_byte = valid_guess_byte
                    break
        curr_dt_block[block_size - byte_index] = valid_correct_byte ^ byte_index
    plain_text_block = bytes(prev_ct_byte ^ curr_dt_byte for prev_ct_byte, curr_dt_byte in zip(prev_ct_block, curr_dt_block))
    return plain_text_block

def padding_oracle_attack(rem: remote, ct: bytes, until_text: str, valid_text: str, block_size: int = 16, default_byte_value: int = 0) -> bytes:
    pt = bytearray()
    block_count = len(ct) // block_size
    for block_index in trange(1, block_count):
        prev_ct_block = ct[(block_index - 1) * block_size : block_index * block_size]
        curr_ct_block = ct[block_index * block_size : (block_index + 1) * block_size]
        pt.extend(get_plain_text_block(rem, prev_ct_block, curr_ct_block, until_text, valid_text, block_size, default_byte_value))
    return pt

def solution(host: str, port: str) -> str:
    context.update({"log_level": "error"})
    N = 16
    with remote(host, port) as rem:
        original = bytes.fromhex(rem.recvline().strip().decode())
        flag = get_flag(padding_oracle_attack(rem, original, "> ", "Valid padding", N, 0).decode(), "watctf")
    return flag

if __name__ == "__main__":
    host = "challs.watctf.org"
    port = "2013"
    print(solution(host, port))
    