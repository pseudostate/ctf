from sage.all import PolynomialRing, ZZ, Zmod, factor, gcd
from Crypto.Util.number import long_to_bytes

def solution(random_numbers: list[int]) -> str:
    '''
    seed_1 ≡ a * flag + c (mod m)
    seed_2 ≡ a * seed_1 + c ≡ a * (a * seed_1 + c) + c ≡ a ** 2 * seed_1 + a * c + c ≡ a ** 2 * seed_1 + c  (a + 1) (mod m)
    seed_3 ≡ a * seed_2 + c ≡ a * (a ** 2 * seed_2 + c(a + 1)) + c ≡ a ** 3 * seed_2 + c * (a ** 2 + a + 1) (mod m)
    ...
    seed_k ≡ a ** k * seed_(k-1) + c * (a ** (k - 1) + a ** (k - 2) + ... + 1) (mod m)

    temp = a ** (k - 1) + a ** (k - 2) + ... + 1
    a * temp = a ** k + a ** (k - 1) + ... + a
    a * temp - temp = a ** k - 1
    (a - 1) * temp = a ** k - 1
    temp = (a ** k - 1) / (a - 1)

    ∴ seed_k ≡ a ** k * seed_(k-1) + c * (a ** k - 1) / (a - 1) (mod m)
    (a - 1) * seed_k ≡ (a - 1) * (a ** k * seed_(k-1)) + c * (a ** k - 1) (mod m)
    c * (a ** k - 1) ≡ (a - 1) * seed_k - (a - 1) * (a ** k * seed_(k-1)) (mod m)
    c * (a ** k - 1) ≡ (a - 1) * (seed_k - (a ** k * seed_(k-1))) (mod m) ... ①

    seed_(k+1) ≡ a ** (k + 1) * seed_k + c * (a ** (k + 1) - 1) / (a - 1) (mod m)
    (a - 1) * seed_(k+1) ≡ (a - 1) * (a ** (k + 1) * seed_k) + c * (a ** (k + 1) - 1) (mod m)
    c * (a ** (k + 1) - 1) ≡ (a - 1) * seed_(k+1) - (a - 1) * (a ** (k + 1) * seed_k) (mod m)
    c * (a ** (k + 1) - 1) ≡ (a - 1) * (seed_(k+1) - (a ** (k + 1) * seed_k)) (mod m) ... ②

    ① * (a ** (k + 1) - 1) ≡ ② * (a ** k - 1) (mod m)
    c * (a ** k - 1) * (a ** (k + 1) - 1) ≡ (a ** (k + 1) - 1) * (a - 1) * (seed_k - (a ** k * seed_(k-1))) (mod m)
    c * (a ** (k + 1) - 1) * (a ** k - 1) ≡ (a ** k - 1) * (a - 1) * (seed_(k+1) - (a ** (k + 1) * seed_k)) (mod m)
    
    (a ** k - 1) * (a - 1) * (seed_(k+1) - (a ** (k + 1) * seed_k)) ≡ (a ** (k + 1) - 1) * (a - 1) * (seed_k - (a ** k * seed_(k-1))) (mod m)
    (a ** k - 1) * (a - 1) * (seed_(k+1) - (a ** (k + 1) * seed_k)) ≡ 0 (mod (a - 1) ** 2) ... ③
    (a ** (k + 1) - 1) * (a - 1) * (seed_k - (a ** k * seed_(k-1))) ≡ 0 (mod (a - 1) ** 2) ... ④

    ③ / (a - 1) ** 2 = (a ** (k - 1) + ... + 1) * (seed_(k+1) - (a ** (k + 1) * seed_k)) ... ⑤
    ④ / (a - 1) ** 2 = (a ** k + ... + 1) * (seed_k - (a ** k * seed_(k-1))) ... ⑥

    ⑤ - ⑥ ≡ 0 (mod m)
    k = 2 -> ⑤ - ⑥ ... ⑦
    k = 3 -> ⑤ - ⑥ ... ⑧
    k = 4 -> ⑤ - ⑥ ... ⑨
    ...
    m = gcd(resultant(⑦, ⑧), resultant(⑧, ⑨), ...)'s big factor
    a = ⑦ and ⑧ share root
    c = ①(k = 2)
    flag = (seed_1 - c) * (a ** -1) (mod m)
    '''
    polynomial_list = []
    a = PolynomialRing(ZZ, "a").gen()
    for k in range(2, len(random_numbers)):
        seed_prev_k = random_numbers[k - 2]
        seed_curr_k = random_numbers[k - 1]
        seed_next_k = random_numbers[k]
        left = (a ** k - 1) * (a - 1) * (seed_next_k - (a ** (k + 1) * seed_curr_k))
        right = (a ** (k + 1) - 1) * (a - 1) * (seed_curr_k - (a ** k * seed_prev_k))
        polynomial_list.append((left - right) // ((a - 1) ** 2))

    for polynomial_index in range(1, len(polynomial_list)):
        if polynomial_index == 1:
            g = polynomial_list[polynomial_index - 1].resultant(polynomial_list[polynomial_index])
        else:
            g = gcd(g, polynomial_list[polynomial_index - 1].resultant(polynomial_list[polynomial_index]))

    for p, e in factor(g):
        if p.bit_length() >= len("amateursCTF{.}"):
            m = p
            break
    a_mod_m = PolynomialRing(Zmod(m), "a").gen()
    roots = a_mod_m(polynomial_list[0]).roots(multiplicities = False)
    for a_candidate in roots:
        if a_mod_m(polynomial_list[1])(a_candidate) == 0:
            a = int(a_candidate)
            break
            
    c = (((a - 1) * random_numbers[1] - (a ** 2) * (a - 1) * random_numbers[0]) * pow(a ** 2 - 1, -1, m)) % m
    plain = ((random_numbers[0] - c) * pow(a, -1, m)) % m
    flag = long_to_bytes(plain).decode()
    return flag

if __name__ == "__main__":
    random_numbers = [
        1471207943545852478106618608447716459893047706734102352763789322304413594294954078951854930241394509747415,
        1598692736073482992170952603470306867921209728727115430390864029776876148087638761351349854291345381739153,
        7263027854980708582516705896838975362413360736887495919458129587084263748979742208194554859835570092536173,
        1421793811298953348672614691847135074360107904034360298926919347912881575026291936258693160494676689549954,
        7461500488401740536173753018264993398650307817555091262529778478859878439497126612121005384358955488744365,
        7993378969370214846258034508475124464164228761748258400865971489460388035990421363365750583336003815658573
    ]
    print(solution(random_numbers))