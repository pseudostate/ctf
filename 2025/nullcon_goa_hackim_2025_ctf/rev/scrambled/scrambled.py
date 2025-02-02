import random

def decrypt(scrambled_result: list[bytes]) -> str:
    for key in range(0x100):
        decrypt_text = ""
        for b in scrambled_result:
            value = b ^ key
            if value < 0x20 or value > 0x7E:
                break
            decrypt_text += chr(value)
        else:
            if decrypt_text.count("ENO{") > 0:
                return decrypt_text
    return None

def restore(decrypt_text: str) -> str:
    for seed in range(11):
        chunk_size = 4
        chunks = [decrypt_text[i : i + chunk_size] for i in range(0, len(decrypt_text), chunk_size)]
        original_chunks = chunks[:]
        random.seed(seed)
        random.shuffle(chunks)
        restore_index_mapping = [chunks.index(original_chunk) for original_chunk in original_chunks]
        restore_flag = "".join(original_chunks[i] for i in restore_index_mapping)
        if restore_flag.startswith("ENO{") and restore_flag.endswith("}"):
            return restore_flag

def solution(scrambled_result: str) -> str:
    scrambled_result = ""
    with open(file_name, "r") as f:
        scrambled_result = f.readline().strip().split(": ")[1]
    decrypt_text = decrypt([int(scrambled_result[i : i + 2], 16) for i in range(0, len(scrambled_result), 2)])
    return restore(decrypt_text)

if __name__ == "__main__":
    file_name = "output.txt"
    print(solution(file_name))
    