# pip install bcrypt==4.2.0 --force-reinstall
import os, base64, bcrypt, string
from pwn import context, remote
from itertools import product
from multiprocessing import Pool
from functools import partial

def vibe_hash(data: str) -> str:
    _STATIC_SALT = b"$2b$12$C8YQMlqDyz3vGN9VOGBeGu"
    payload = data.encode("utf-8")
    portion = payload[: len(payload) % 256]
    digest = bcrypt.hashpw(portion, _STATIC_SALT)
    return f"vb$1${base64.b64encode(digest).decode()}"

def parallel_brute_force(c1_c2: tuple[str, str], leak_note: str, target_hash: str) -> str | None:
    password = None
    c1, c2 = c1_c2
    candidate = leak_note + c1 + c2
    if vibe_hash(candidate) == target_hash:
        password = candidate
    return password

def level_1(leak_note: str, target_hash: str) -> str:
    password = None
    permutation_with_repetition = product(string.ascii_letters + string.digits, repeat = 2)
    with Pool(processes = os.cpu_count()) as pool:
        for result in pool.imap_unordered(partial(parallel_brute_force, leak_note = leak_note, target_hash = target_hash), permutation_with_repetition):
            if result:
                password = result
                break
    return password

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        # level 1
        rem.recvuntil(b"Leaked Note: ")
        leak_note = rem.recvline().strip().decode()
        rem.recvuntil(b"Target Hash: ")
        target_hash = rem.recvline().strip().decode()
        rem.sendlineafter(b"Enter password: ", level_1(leak_note, target_hash).encode())
        
        # level 2
        rem.recvuntil(b"prefix: '")
        prefix = rem.recvuntil(b"'", drop = True).decode()
        rem.sendlineafter(b"Format: string1,string2", f"{prefix}{"A" * (256 - len(prefix))},{prefix}{"B" * (256 - len(prefix))}".encode())

        # level 3
        rem.recvuntil(b"very long (")
        target_len = int(rem.recvuntil(b" ", drop = True))
        rem.sendlineafter(b"equivalent password: ", ("B" * (target_len % 256)).encode())

        # level 4
        rem.recvuntil(b"password is: ")
        pad_len = int(rem.recvuntil(b"'C's + ", drop = True))
        emoji_count = int(rem.recvuntil(" '🔥' emojis.".encode(), drop = True))
        rem.sendlineafter(b"Enter password: ", ("C" * pad_len + "🔥" * emoji_count).encode()[:72])

        # level 5
        rem.recvuntil(b'ID: "')
        prefix = rem.recvuntil(b'"', drop=True).decode()
        rem.recvuntil(b"SecretPassword: ")
        pad_len = int(rem.recvuntil(b" 'X' characters.", drop = True))
        rem.recvuntil(b"Total Length = ")
        total_len = int(rem.recvuntil(b" ", drop = True))
        need_X_count = (total_len - len(prefix)) % 256
        rem.sendlineafter(b"Input your password:", b"X" * need_X_count)

        rem.recvuntil(b"Here is your reward: ")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "18.212.136.134"
    port = "6666"
    print(solution(host, port))
