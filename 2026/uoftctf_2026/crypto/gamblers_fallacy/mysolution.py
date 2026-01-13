import hashlib, hmac
from pwn import context, remote
from randcrack import RandCrack

def roll_dice(server_seed: int, client_seed: int, nonce: int) -> int:
    nonce_client_msg = f"{client_seed}-{nonce}".encode()
    sig = hmac.new(str(server_seed).encode(), nonce_client_msg, hashlib.sha256).hexdigest()
    index = 0
    lucky = int(sig[index*5:index*5+5], 16)
    while (lucky >= 1e6):
        index += 1
        lucky = int(sig[index * 5:index * 5 + 5], 16)
        if (index * 5 + 5 > 129):
            lucky = 9999
            break
    return round((lucky % 1e4) * 1e-2)

def get_current_balance(rem: remote) -> float:
    rem.sendlineafter(b"> ", b"c")
    rem.recvuntil(b"current seed: ")
    client_seed = rem.recvline().strip().decode()
    rem.sendlineafter(b"Set custom seed: ", client_seed.encode())
    rem.recvuntil(b"Balance: ")
    return float(rem.recvline().strip().decode())

def gamble(rem: remote, wager: float, games: int, number: int) -> list[int]:
    server_seeds = []
    rem.sendlineafter(b"> ", b"b")
    rem.recvuntil(b"Wager per game (min-wager is ")
    rem.sendlineafter(b"): ", str(wager).encode())
    rem.sendlineafter(b"Number of games (int): ", str(games).encode())
    rem.sendlineafter(b"Enter your number higher or equal to the roll between 2-98 (prize improves with lower numbers): ", str(number).encode())
    rem.sendlineafter(b"Do you wish to proceed? (Y/N)", b"Y")
    for game in range(games):
        rem.recvuntil(b"Server-Seed: ")
        server_seeds.append(int(rem.recvline().strip().decode()))
    return server_seeds

def crack_gamble(rem: remote, rc: RandCrack, client_seed: str, current_balance: float, nonce: int) -> None:
    predicted_server_seed = rc.predict_getrandbits(32)
    predicted_roll = roll_dice(predicted_server_seed, client_seed, nonce)
    if 2 <= predicted_roll <= 98:
        gamble(rem, current_balance, 1, predicted_roll)
    else:
        gamble(rem, 1.0, 1, 2)

def buy_flag(rem: remote) -> str:
    rem.sendlineafter(b"> ", b"a")
    rem.sendlineafter(b"> ", b"a")
    flag = rem.recvline().strip().decode()
    return flag

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    randcrack = RandCrack()
    client_seed = "1337awesome"
    balance = 0
    current_nonce = 0
    with remote(host, port) as rem:
        rem.recvuntil(b"Balance: ")
        balance = float(rem.recvline().strip().decode())
        game_count = 624
        server_seeds = gamble(rem, 1.0, game_count, 2)
        current_nonce += game_count
        for seed in server_seeds:
            randcrack.submit(seed)
        while get_current_balance(rem) < 10000.0:
            crack_gamble(rem, randcrack, client_seed, balance, current_nonce)
            current_nonce += 1
        flag = buy_flag(rem)
    return flag

if __name__ == "__main__":
    host = "34.162.20.138"
    port = "5000"
    print(solution(host, port))
    