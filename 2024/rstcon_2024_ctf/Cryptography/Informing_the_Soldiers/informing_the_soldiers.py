def solution(sentence: str) -> None:
    for shift in range(26):
        plain = ""
        for letter in sentence:
            if letter.isupper():
                plain += chr((ord(letter) - ord('A') - shift) % 26 + ord('A'))
            elif letter.islower():
                plain += chr((ord(letter) - ord('a') - shift) % 26 + ord('a'))
            else:
                plain += letter
        if plain[:4] == "Meta":
            print(plain)

if __name__ == "__main__":
    sentence = "ZrgnPGS{napvrag_pvcuref_sgj)"
    solution(sentence)
    