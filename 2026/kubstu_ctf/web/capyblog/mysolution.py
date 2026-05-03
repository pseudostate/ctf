import os, requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\(.*?\)", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        flag = get_flag(ses.get(f"{url}").text, prefix)
    return flag

if __name__ == "__main__":
    url = "http://159.194.209.128"
    prefix = "KubSTU"
    while (flag := solution(url, prefix)) == None:
        continue
    print(flag)
        