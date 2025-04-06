import os
from pwn import *

def get_data(file_name: str) -> str:
    data = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        data = f.read()
    return data

def solution(host: str, port: str, output_file_name: str) -> str:
    flag = ""
    output_data = get_data(output_file_name)
    output = int(output_data)
    context.update({"arch":"amd64","log_level":"error"})
    with remote(host, port) as r:
        r.recvuntil(b"Input your number: ")
        r.sendline(str(output).encode())
        r.recvuntil(b"Here is the flag: ")
        flag = r.recvline().decode().strip()
    return flag

if __name__ == "__main__":
    host = "challs.breachers.in"
    port = "13337"
    output_file_name = "output.txt"
    print(solution(host, port, output_file_name))
    