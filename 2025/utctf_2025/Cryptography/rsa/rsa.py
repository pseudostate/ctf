import os, gmpy2

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            key, value = line.strip().split(": ")
            data[key] = int(value)
    return data

def solution(file_name: str) -> str:
    data = get_data(file_name)
    c = data["c"]
    e = data["e"]
    m = gmpy2.iroot(c, e)[0] # c = m^e % n -> (use small e) -> c = m^e
    flag = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big").decode()
    return flag

if __name__ == "__main__":
    file_name = "rsa.txt"
    print(solution(file_name))
    