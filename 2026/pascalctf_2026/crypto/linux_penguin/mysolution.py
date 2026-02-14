from pwn import context, remote

def solution(host: str, port: str, words: list[str]) -> str:
    context.update({"log_level":"error"})
    encrypted_words = []
    with remote(host, port) as rem:
        for i, word in enumerate(words):
            rem.sendlineafter(b": ", word.encode())
            if i % 4 == 3:
                rem.recvuntil(b"Encrypted words: ")
                encrypted_words.extend(rem.recvline().strip().decode().split(" "))
        rem.recvuntil(b"Ciphertext: ")
        cipher_texts = rem.recvline().strip().decode().split(" ")
        for cipher_text in cipher_texts:
            rem.sendlineafter(b": ", words[encrypted_words.index(cipher_text)].encode())
        rem.recvuntil(b"pascalCTF")
        flag = "pascalCTF" + rem.recvline().strip().decode()
    return flag

if __name__ == "__main__":
    host = "penguin.ctf.pascalctf.it"
    port = "5003"
    words = [
        "biocompatibility", "biodegradability", "characterization", "contraindication",
        "counterbalancing", "counterintuitive", "decentralization", "disproportionate",
        "electrochemistry", "electromagnetism", "environmentalist", "internationality",
        "internationalism", "institutionalize", "microlithography", "microphotography",
        "misappropriation", "mischaracterized", "miscommunication", "misunderstanding",
        "photolithography", "phonocardiograph", "psychophysiology", "rationalizations",
        "representational", "responsibilities", "transcontinental", "unconstitutional"
    ]
    print(solution(host, port, words))
    