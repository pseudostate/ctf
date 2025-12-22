import re, string, itertools, numpy as np
from pwn import context, remote
from hashlib import sha256, md5

def proof_of_work_solution(rem: remote) -> None:
    rem.recvuntil(b"sha256(")
    sha256_prefix = rem.recvuntil(b" + ???) starts with ", drop = True).strip().decode()
    hash_prefix = rem.recvline().strip().decode()
    length = 1
    while True:
        for product in itertools.product(string.ascii_letters + string.digits, repeat = length):
            sha256_suffix = "".join(product)
            if sha256((sha256_prefix + sha256_suffix).encode()).hexdigest().startswith(hash_prefix):
                rem.sendlineafter(b"Enter your answer: ", sha256_suffix.encode())
                return
        length += 1

def get_probability(prev_sub_vector: list[int], target_value: int) -> float:
    total_nums = 20000
    seed = md5(str(prev_sub_vector).encode()).hexdigest()
    seed_int = int(seed, 16)
    rng = np.random.default_rng(seed_int)
    us = rng.random(total_nums)
    return float(us[target_value])

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"log_level":"error"})
    window = 5
    play_times = 200
    with remote(host, port) as rem:
        proof_of_work_solution(rem)
        for _ in range(play_times):
            rem.recvuntil(b"Vector: ")
            vector = eval(rem.recvline().strip().decode())
            probabilities = []
            for i in range(window, len(vector)):
                prev_sub_vector = vector[i - window : i]
                target_value = vector[i]
                probability = get_probability(prev_sub_vector, target_value)
                probabilities.append(probability)
            if sum(1 for p in probabilities if p > 0.999) > 1:
                user_bit = 0
            else:
                user_bit = 1
            rem.sendlineafter(b"Please tell me the bit of the vector", str(user_bit).encode())
        rem.recvuntil(b"You are a good guesser, the flag is ")
        flag = rem.recvline().strip().decode()
    return get_flag(flag, prefix)

if __name__ == "__main__":
    host = "instance.penguin.0ops.sjtu.cn"
    port = "18396"
    prefix = "0ops"
    print(solution(host, port, prefix))
