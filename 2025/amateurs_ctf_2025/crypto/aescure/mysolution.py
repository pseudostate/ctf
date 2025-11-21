import os, string
from Crypto.Cipher import AES
from itertools import product
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial

def brute_force(guess_bytes: bytes, c: bytes, p: bytes, prefix: bytes, suffix: bytes) -> str | None:
    try:
        key = prefix + bytes(guess_bytes) + suffix
        if AES.new(key, AES.MODE_ECB).decrypt(c) == p:
            return key.decode()
    except:
        pass
    return None

def solution(c: bytes, p: bytes, prefix: bytes, suffix: bytes) -> str:
    '''
    key length = 16 bytes or 24 bytes or 32 bytes
    16 bytes -> amateursCTF{???}
    24 bytes -> amateursCTF{???????????}
    32 bytes -> amateursCTF{???????????????????}
    '''
    unknown_length = 16 - len(prefix) - len(suffix) # 16 or 24 or 32
    character_set = string.printable
    permutation_with_repetition = product(character_set.encode(), repeat = unknown_length)
    total = len(character_set) ** unknown_length
    with Pool(processes = os.cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(partial(brute_force, c = c, p = p, prefix = prefix, suffix = suffix), permutation_with_repetition, chunksize = 10000), total = total):
            if result:
                flag = result
                break
    return flag

if __name__ == "__main__":
    c = bytes.fromhex("5aed095b21675ec4ceb770994289f72b")
    p = b"\x00" * 16
    prefix = b"amateursCTF{"
    suffix = b"}"
    print(solution(c, p, prefix, suffix))
