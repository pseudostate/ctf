from pwn import remote, context
from decimal import Decimal, getcontext

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    getcontext().prec = 1000
    e = 0x10001
    mapping = {"Null": 0, "Eins": 1, "Zwei": 2, "Drei": 3}
    with remote(host, port) as rem:
        n = int(rem.recvline().strip().decode())
        c = int(rem.recvline().strip().decode())

        low = Decimal(0)
        high = Decimal(n)
        curr_c = c

        rem.sendlineafter(b"> ", str(curr_c).encode())
        output = rem.recvline().strip().decode()
        while "Interesting..." not in output:
            result = mapping[output]
            diff = (high - low) / 4
            low, high = low + diff * result, low + diff * (result + 1)

            if int(high) - int(low) <= 1:
                curr_c = int(high)
            else:
                curr_c = (curr_c * pow(4, e, n)) % n
            rem.sendlineafter(b"> ", str(curr_c).encode())
            output = rem.recvline().strip().decode()
        flag = rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "host8.dreamhack.games"
    port = "8829"
    print(solution(host, port))
    