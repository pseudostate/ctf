import os
from Crypto.Util.number import bytes_to_long, long_to_bytes

def get_data(encrypted_file: str) -> int:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), encrypted_file), "rb") as f:
        data = bytes_to_long(f.read())
    return data

def solution(encrypted_file: str) -> str:
    data = get_data(encrypted_file)
    o = ((6, 0, 7), (8, 2, 1), (5, 4, 3))
    inv_map = {val: (r, c) for r, row in enumerate(o) for c, val in enumerate(row)}
    
    base9_digits = []
    while data > 0:
        data, rem = divmod(data, 9)
        base9_digits.append(rem)
    base9_digits.reverse()

    n = len(base9_digits)
    trits = [0] * (n * 2)

    for i, val in enumerate(base9_digits):
        row, col = inv_map[val]
        trits[i] = row
        trits[2 * n - 1 - i] = col

    plain = 0
    for t in trits:
        plain = plain * 3 + t

    flag = long_to_bytes(plain).decode()
    return flag

if __name__ == "__main__":
    encrypted_file = "encrypted"
    print(solution(encrypted_file))
    