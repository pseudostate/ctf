from pwn import context, remote

def check_quadratic_residue(a: int, p: int) -> bool:
    return pow(a, (p - 1) // 2, p) == 1

def solution(host: str, port: str) -> str:
    context.update({"log_level":"debug"})
    with remote(host, port) as rem:
        rem.recvuntil(b"The Mystical El-Camel is in town!\nBeat their game to win a special prize...\n\n")
        p = int(rem.recvline().strip().decode())
        q = int(rem.recvline().strip().decode())
        rem.sendlineafter(b"How tall do you want the coin to be?> ", str(0).encode())
        rem.sendlineafter(b"How long do you want the coin to be?> ", str(1).encode())
        for _ in range(50):
            c = int(rem.recvline().strip().decode())
            guess = "H" if check_quadratic_residue(c, p) else "T"
            rem.sendlineafter(b"Heads or Tails! (H or T)> ", guess.encode())
            rem.recvuntil(b"\n\n")
        rem.recvline_contains(b"ElCamel is impressed! Here is your prize...\n")
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "challenge.secso.cc"
    port = "7001"
    print(solution(host, port))
    