import os, ecdsa, hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from Crypto.Util.number import long_to_bytes
from pwn import xor

def get_public_key(pem_file: str) -> ec.EllipticCurvePublicKey:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), pem_file), "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def get_signature_data(signature_file_name: str, delimit: str) -> dict[str, int]:
    data = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), signature_file_name), "r") as f:
        for line in f:
            if delimit in line:
                key, value = line.strip().split(delimit)
                data[key] = int(value, 16)
    return data

def get_blob_data(blob_file_name: str) -> bytes:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), blob_file_name), "rb") as f:
        data = f.read()
    return data

def calculate_private_key(r: int, s1: int, s2: int, z1: int, z2: int, n: int) -> int:
    '''
    private_key = (s2 * z1 - s1 * z2) / (r * (s1 - s2))
    s1 = sign(message1)
    s2 = sign(message2)
    z1 = bytes_to_long(message1)
    z2 = bytes_to_long(message2)
    '''
    return (((s2 * z1 - s1 * z2) % n) * (pow(r * (s1 - s2), -1, n))) % n

def decrypt(private_key: int, secret_blob_file: str) -> str:
    key_stream = []
    for ctr in range(len(secret_blob_file) // len(long_to_bytes(private_key)) + 1):
        key_stream.extend(hashlib.sha256(long_to_bytes(private_key) + long_to_bytes(ctr, 4)).digest())
    return xor(bytes(key_stream[:len(secret_blob_file)]), secret_blob_file).strip().decode()

def solution(public_pem_file: str, secret_blob_file: str, signature_file_1: str, signature_file_2: str, delimit: str) -> str:
    public_key = get_public_key(public_pem_file)
    n = int(ecdsa.curves.curve_by_name(public_key.curve.name).order)
    signature1 = get_signature_data(signature_file_1, delimit)
    signature2 = get_signature_data(signature_file_2, delimit)
    private_key = calculate_private_key(signature1["r"], signature1["s"], signature2["s"], signature1["msg_hash"], signature2["msg_hash"], n)
    blob_data = get_blob_data(secret_blob_file)
    flag = decrypt(private_key, blob_data)
    return flag

if __name__ == "__main__":
    public_pem_file = "pub.pem"
    secret_blob_file = "secret_blob.bin"
    signature_file_1 = "sig1.txt"
    signature_file_2 = "sig2.txt"
    delimit = ": "
    print(solution(public_pem_file, secret_blob_file, signature_file_1, signature_file_2, delimit))
    