from sage.all import is_prime, factor, GF, discrete_log, gcd
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from hashlib import md5

def solution(alice_public_key: tuple[int, int], bob_public_key: tuple[int, int], encrypted_flag: bytes) -> str:
    ax, ay = alice_public_key
    bx, by = bob_public_key
    p = gcd(ax ** 2 + ay ** 2 - 1, bx ** 2 + by ** 2 - 1) # x ** 2 + y ** 2 - 1 = k * p
    if not is_prime(p):
        p = max([f for f, e in factor(p)])
    Fp = GF(p)
    i = Fp(-1).sqrt() # i ** 2 = -1

    base_x = Fp(13187661168110324954294058945757101408527953727379258599969622948218380874617)
    base_y = Fp(5650730937120921351586377003219139165467571376033493483369229779706160055207)
    mapped_base = base_y + base_x * i
    mapped_alice_public = Fp(ay) + Fp(ax) * i
    mapped_bob_public = Fp(by) + Fp(bx) * i
    alice_secret = discrete_log(mapped_alice_public, mapped_base)
    shared_value = mapped_bob_public ** alice_secret
    
    coords = shared_value.list()
    shared_y, shared_x = int(coords[0]), int(coords[1])
    key = md5(f"{shared_x},{shared_y}".encode()).digest()
    flag = AES.new(key, AES.MODE_ECB).decrypt(encrypted_flag).decode()
    return flag

if __name__ == "__main__":
    alice_public_key = (13109366899209289301676180036151662757744653412475893615415990437597518621948, 5214723011482927364940019305510447986283757364508376959496938374504175747801)
    bob_public_key = (1970812974353385315040605739189121087177682987805959975185933521200533840941, 12973039444480670818762166333866292061530850590498312261363790018126209960024)
    encrypted_flag = bytes.fromhex("d345a465538e3babd495cd89b43a224ac93614e987dfb4a6d3196e2d0b3b57d9")
    print(solution(alice_public_key, bob_public_key, encrypted_flag))
