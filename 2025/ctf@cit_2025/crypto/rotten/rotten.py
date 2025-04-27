def decode_rot(cipher_text: str, n: int = 13) -> str:
    plain_text = ""
    for c in cipher_text:
        if "A" <= c <= "Z":
            plain_text += chr((ord(c) - ord("A") + n) % 26 + ord("A"))
        elif "a" <= c <= "z":
            plain_text += chr((ord(c) - ord("a") + n) % 26 + ord("a"))
        else:
            plain_text += c
    return plain_text

def solution(cipher_text: str, prefix: str) -> str:
    flag = ""
    for n in range(26):
        plain_text = decode_rot(cipher_text, n)
        if plain_text.upper().startswith(prefix):
            flag = plain_text
            break
    return flag

if __name__ == "__main__":
    cipher_text = "PVG{LxxdJwAXJGcsDoncKfRctddA}"
    prefix = "CIT{"
    print(solution(cipher_text, prefix))
    