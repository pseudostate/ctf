import os, gmpy2

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    data["tung"] = 0
    data["sahur"] = 0
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            if line.find("Tung!") >= 0:
                data["tung"] += 1
            elif line.find("Sahur!") >= 0:
                data["sahur"] += 1
            else:
                key, value = line.strip().split(" = ")
                data[key] = int(value)
    return data

def solution(file_name: str) -> str:
    data = get_data(file_name)
    n = data["N"]
    e = data["e"]
    c = data["C"]
    tung = data["tung"]
    sahur = data["sahur"]
    while sahur > 0:
        c += n
        sahur -= 1
    while tung > 0:
        c //= 2
        tung -= 1
    m = gmpy2.iroot(c, e)[0]
    flag = bytes.fromhex(hex(m)[2:]).decode()
    return flag

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    