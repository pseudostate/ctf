import os, string

def get_data(file_name: str) -> str:
    data = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        data = f.read()
    return data

def get_only_alphabet(s: str) -> str:
    return "".join(c for c in s if c in string.ascii_lowercase)

def g(c, k):
    c = ord(c) - ord("a")
    k = ord(k) - ord("a")
    ret = (c - k) % 26
    return chr(ord("a") + ret)

def decrypt_vigenere(cipher_text: str, key: str) -> str:   
    idx = 0
    plain_text = []
    plain_text_without_symbols = []
    for c in cipher_text:
        if c in string.ascii_lowercase:
            if idx < len(key):
                k = key[idx]
            else:
                k = plain_text_without_symbols[idx-len(key)]
            plain_text_without_symbols.append(g(c, k))
            plain_text.append(g(c, k))
            idx += 1          
        else:
            plain_text.append(c)
    plain_text = "".join(c for c in plain_text)
    return plain_text

def solution(output_file_name: str) -> str:
    cipher_text = get_data(output_file_name).split("\"")[1]
    return decrypt_vigenere(cipher_text, "ahxybmqh" + get_only_alphabet(cipher_text)[:-8])

if __name__ == "__main__":
    output_file_name = "output.txt"
    print(solution(output_file_name))
    