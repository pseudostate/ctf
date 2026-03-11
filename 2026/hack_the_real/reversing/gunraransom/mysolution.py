import os, re, datetime, random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def get_data(reference_file: str) -> bytes:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), reference_file), "rb") as f:
        data = f.read()
    return data

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(reference_file: str, prefix: str) -> str:
    encrypted_data = get_data(reference_file)
    block_size = 16
    iv, ct = encrypted_data[:block_size], encrypted_data[block_size:]
    start_time = int(datetime.datetime(2025, 10, 1, 8, 40, 10, tzinfo = datetime.timezone(datetime.timedelta(hours = 9))).timestamp())
    end_time = int(datetime.datetime(2025, 10, 1, 23, 59, 59, tzinfo = datetime.timezone(datetime.timedelta(hours = 9))).timestamp())
    for time_stamp in range(start_time, end_time + 1):
        r = random.Random(time_stamp)
        key = bytes([r.randint(0, 255) for _ in range(32)])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        try:
            decrypted_data = unpad(cipher.decrypt(ct), block_size).decode()
            flag = get_flag(decrypted_data, prefix)
            if flag != "":
                break
        except:
            continue
    return flag

if __name__ == "__main__":
    reference_file = "encrypted.bin"
    prefix = "EQST"
    print(solution(reference_file, prefix))