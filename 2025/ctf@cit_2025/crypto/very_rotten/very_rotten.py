import base64

def decode_rot(cipher_text: str, n: int = 13) -> str:
    plain_text = ""
    for c in cipher_text:
        if "A" <= c <= "Z":
            plain_text += chr((ord(c) - ord("A") + n) % 26 + ord("A"))
        elif "a" <= c <= "z":
            plain_text += chr((ord(c) - ord("a") + n + 5) % 26 + ord("a"))
        elif "0" <= c <= "9":
            plain_text += chr((ord(c) - ord("0") + n + 10) % 10 + ord("0"))
        else:
            plain_text += c
    return plain_text

def solution(cipher_text: str, prefix: str) -> str:
    flag = ""
    cipher_text = base64.b64decode(cipher_text).decode()
    for n in range(26):
        plain_text = decode_rot(cipher_text, n)
        if plain_text.upper().startswith(prefix):
            flag = plain_text
            break
    return flag

if __name__ == "__main__":
    cipher_text = "TFJDe0gzeV9ldmlfdzMzX0FYQ0M2V19Wa1hidldINDYxTXR1YlgyOXZnYn0="
    prefix = "CIT{"
    print(solution(cipher_text, prefix))
    