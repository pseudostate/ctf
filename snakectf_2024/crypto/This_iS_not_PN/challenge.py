import os
from hashlib import sha1


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def util_encrypt(plaintext, key):
    return byte_xor(plaintext, sha1(key).digest())


# plaintext of 32 bytes, ciphertext of 32 bytes
def encrypt(plaintext, key, nrounds):
    tweaks_1 = [os.urandom(16) for _ in range(nrounds)]
    tweaks_2 = [os.urandom(16) for _ in range(nrounds)]

    p1 = plaintext[:16]
    p2 = plaintext[16:]

    for i in range(nrounds):
        p2_temp = byte_xor(p1, tweaks_1[i])
        p1_temp = byte_xor(byte_xor(p2, tweaks_2[i]), util_encrypt(p2_temp, key))
        p1 = p1_temp
        p2 = p2_temp

    return p1 + p2, tweaks_1, tweaks_2


def decrypt(ciphertext, key, nrounds, tweaks_1, tweaks_2):
    c1 = ciphertext[:16]
    c2 = ciphertext[16:]

    for i in range(nrounds - 1, -1, -1):
        c1_temp = byte_xor(c2, tweaks_1[i])
        c2_temp = byte_xor(byte_xor(c1, tweaks_2[i]), util_encrypt(c2, key))
        c1 = c1_temp
        c2 = c2_temp

    return c1 + c2


def main(FLAG):
    assert len(FLAG) == 32

    p = FLAG.encode()

    # first ciphertext
    key = os.urandom(16)
    nrounds = 5
    c_5round, t1, t2 = encrypt(p, key, nrounds)
    t1_5round = [el.hex() for el in t1]
    t2_5round = [el.hex() for el in t2]

    # second ciphertext
    key = os.urandom(16)
    nrounds = 6
    c_6round, t1, t2 = encrypt(p, key, nrounds)
    t1_6round = [el.hex() for el in t1]
    t2_6round = [el.hex() for el in t2]

    return c_5round.hex(), t1_5round, t2_5round, c_6round.hex(), t1_6round, t2_6round


if __name__ == '__main__':
    print(main("flag{this_is_a_fake_flag.......}"))
