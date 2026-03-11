from pwn import context, remote

def solution(host: str, port: str) -> str:
    context.update({"log_level":"error"})
    with remote(host, port, typ = "udp") as rem:
        rem.sendline(b"\x72\x55")
        flag = rem.recv(1024).strip().decode()
    return flag

if __name__ == "__main__":
    host = "lab.eqst.co.kr"
    port = "8165"
    print(solution(host, port))
    