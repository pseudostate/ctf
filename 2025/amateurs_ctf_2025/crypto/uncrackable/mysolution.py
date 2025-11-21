import os
from pwn import xor

def get_data(file_name: str, flag_length: int) -> dict[str, bytes]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        line = bytes.fromhex(f.read().strip())
        data["enc_rand"] = line[:-flag_length]
        data["enc_flag"] = line[-flag_length:]
    return data

def get_state(enc_rand: bytes, state_length: int) -> bytes:
    recover_state = bytearray(state_length)
    for state_index in range(state_length):
        for guess_byte in range(256):
            possible_byte = True
            for counter in range(state_index, len(enc_rand), state_length):
                if enc_rand[counter] ^ (guess_byte + (counter // state_length)) % 256 in b" \t\n\r":
                    possible_byte = False
                    break
            if possible_byte:
                recover_state[state_index] = guess_byte
    return recover_state

def get_key_flag(enc_rand: bytes, recover_state: bytes, state_length: int, flag_length: int) -> bytes:
    key_flag = bytearray(flag_length)
    for flag_index in range(flag_length):
        data_index = len(enc_rand) + flag_index
        counter = data_index // state_length
        state_index = data_index % state_length
        key_flag[flag_index] = (recover_state[state_index] + counter) % 256
    return key_flag

def solution(file_name: str, state_length: int, flag_length: int) -> str:
    data = get_data(file_name, flag_length)
    enc_rand = data["enc_rand"]
    enc_flag = data["enc_flag"]
    recover_state = get_state(enc_rand, state_length)
    key_flag = get_key_flag(enc_rand, recover_state, state_length, flag_length)
    flag = xor(key_flag, enc_flag).decode()
    if not flag.startswith("amateursCTF"): flag = f"amateursCTF{{{flag}}}" 
    return flag

if __name__ == "__main__":
    file_name = "out.txt"
    state_length = 32
    flag_length = 47
    print(solution(file_name, state_length, flag_length))
