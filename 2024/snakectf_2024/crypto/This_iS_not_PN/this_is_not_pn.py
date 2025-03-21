import binascii
from itertools import product
from challenge import decrypt

def solution(ciphertext: str, nrounds: int, tweaks_1: list[str], tweaks_2: list[str]) -> str:
    ciphertext = binascii.unhexlify(ciphertext)
    tweaks_1 = [binascii.unhexlify(tweak) for tweak in tweaks_1]
    tweaks_2 = [binascii.unhexlify(tweak) for tweak in tweaks_2]
    plaintext = ""
    for key in product(range(256), repeat=16):
        try:
            plaintext = decrypt(ciphertext, bytes(key), nrounds, tweaks_1, tweaks_2).decode("ASCII")
            break
        except:
            pass
    return plaintext

if __name__ == "__main__":
    c_5round_hex = "49f4e8715e6fdf5cceed4db545c95114aec8f7ae13b72cd42272655f202216aa"
    t1_5round = ['512ca66ee6d650aa7d1accaa4d21b63d', '9234f4cabfaa89a5eabdd2064ae7fa4b', 'c8262e06c249ae9f9ed814bf9bdcce58', '27642f8d2c00ae8cef033f6e55ff6c98', 'e072db6d94156f7ef79770337accd4aa']
    t2_5round = ['5198b29509b09d98f4725e3a017b4d1f', 'f00f1436c10cff38e5380954cd43dd63', 'd957cd657500b30d22a62f8bde0dd59e', '7be04c5d462a2350e76ec76a8be48830', '43865c484b66b5d8e45f0f029dd2cc9c']
    print(f"CASE 1 = {solution(c_5round_hex, 5, t1_5round, t2_5round)}")
    c_6round_hex = "172da7231904dca9d39282b080b92aaa9948c8faf79dc4318c05c8628905cf77"
    t1_6round = ['6b46051ab069e5d3e5411961b9bafd81', 'bbe69bcc0f4b1448ff996edeed75ae94', '34fd5f8dc6331eee69c31044fe408677', '75d483ed80698e8d8692ca510704a81a', '22145cf1bdebb39aa8a71d66ea1d57f4', '8e6c98a1d816dd276e4980568636647a']
    t2_6round = ['46f242281fb4953fd37676f518794080', 'bb2a34c83654773318651f65e06541c8', 'ff2904359ddeb9c3f0f42fff12198744', 'fc0d9dc8220d95f14373f6b2ce2a5045', 'd19b7ca5229cb4e70bb5d0d3f41de06a', '55d8cbcbdb745a6f2f9940842d24d5bd']
    print(f"CASE 2 = {solution(c_6round_hex, 6, t1_6round, t2_6round)}")
    