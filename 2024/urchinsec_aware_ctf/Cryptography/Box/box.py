def solution(cipher_text: str) -> None:
    for shift in range(26):
        plain_text = ""
        for letter in cipher_text:
            if letter.isupper():
                plain_text += chr((ord(letter) - ord('A') - shift) % 26 + ord('A'))
            elif letter.islower():
                plain_text += chr((ord(letter) - ord('a') - shift) % 26 + ord('a'))
            else:
                plain_text += letter
        if plain_text[:9] == "urchinsec":
            print(plain_text)

if __name__=="__main__":
    cipher_text = "b__ooltxxio␣_k_␣ieb␣"
    solution(cipher_text)
