try:
    from secret import a,b,FLAG
except: # new sage version on arch broke import .py files :c
    load("secret.py")

p = 0xffffffffffffffffffffffffffffffffffffffffffffff13
F = GF(p)

EC.<G> = EllipticCurve(F, [a, b])

q = EC.order()

bob_secret = randint(1,q-1) 
bob_public = bob_secret*G

try:
    alice_public_x = ZZ(int(input("[mitm] A: ")))
    alice_public = EC.lift_x(alice_public_x)
except:
    exit("Funny user.")

# we can't have you doing a regular ecdhke 😛
k = randint(1,q-1)
R = (bob_secret * alice_public)
secret = int(R.x())
print(f"[mitm] B': {(k*bob_public).xy()}")

import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = hashlib.sha256(str(secret).encode()).digest()[:16]
iv = os.urandom(16)

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ct = cipher.encrypt(pad(FLAG, 16))
data = {"iv": iv.hex(), "ct": ct.hex()}
print(json.dumps(data))
