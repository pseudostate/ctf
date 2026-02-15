import hashlib
from sage.all import GF, EllipticCurve
from Crypto.Cipher import AES, DES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad

def solution(ciphertext: str) -> str:
    p = 1070960903638793793346073212977144745230649115077006408609822474051879875814028659881855169
    a = 0
    b = 19
    Px = 850194424131363838588909772639181716366575918001556629491986206564277588835368712774900915
    Py = 749509706400667976882772182663506383952119723848300900481860146956631278026417920626334886
    Qx = 54250358642669756154015134950152636682437522715786363311759940981383592083045988845753867
    Qy = 324772290891069325219931358863917293864610371020855881775477694333357303867104131696431188

    aes_iv = "7d0e47bb8d111b626f0e17be5a761a14"
    des_iv = "86fd0c44751700d4"

    E = EllipticCurve(GF(p), [a, b])
    P = E(Px, Py)
    Q = E(Qx, Qy)
    d = Q.log(P)

    k = long_to_bytes(d)

    des_key = hashlib.sha256(k + b"MeOwl::DES").digest()[:8]
    cipher_des = DES.new(des_key, DES.MODE_CBC, iv = bytes.fromhex(des_iv))
    unpad_cipher_des = unpad(cipher_des.decrypt(bytes.fromhex(ciphertext)), 8)

    aes_key = hashlib.sha256(k + b"MeOwl::AES").digest()[:16]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv = bytes.fromhex(aes_iv))
    flag = unpad(cipher_aes.decrypt(unpad_cipher_des), 16).decode()
    return flag

if __name__ == "__main__":
    ciphertext = "7d34910bca6f505e638ed22f412dbf1b50d03243b739de0090d07fb097ec0a2ca19158949f32e39cd84adea33d2229556f635237088316d2"
    print(solution(ciphertext))
