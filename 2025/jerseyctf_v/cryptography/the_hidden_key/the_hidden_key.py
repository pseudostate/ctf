import os

def get_data(file_name: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        for line in f:
            values = line.strip().split(": ")
            if len(values) > 1:
                key = values[0]
                if "[" in values[1]:
                    values = values[1].strip("[]").split(", ")
                    data[key] = [int(value) for value in values]
                else:
                    data[key] = int(values[1])
    return data

def find_factors(n: int) -> tuple[int]:
    if n < 4:
        return None
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            q = n // p
            return p, q
    return None

def solution(file_name: str) -> str:
    flag = ""
    data = get_data(file_name)
    n = data["n"]
    e = data["e"]
    ct = data["ct"]
    p, q = find_factors(n)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    for c in ct:
        flag += chr(pow(c, d, n))
    return flag

if __name__ == "__main__":
    file_name = "TheHiddenKey.txt"
    print(solution(file_name))
    