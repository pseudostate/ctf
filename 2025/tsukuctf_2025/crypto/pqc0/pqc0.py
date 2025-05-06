import os, subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

def get_data(file_name: str) -> str:
    data = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        data = f.read()
    return data

def solution(output_file_name: str, openssl_path: str) -> str:
    flag = ""
    data = get_data(output_file_name)
    private_key = data.split("==== private_key ====")[1].split("==== ciphertext(hex) ====")[0].strip()
    cipher_text = int(data.split("==== ciphertext(hex) ====")[1].split("==== encrypted_flag(hex) ====")[0].strip(), 16)
    encrypted_flag = int(data.split("==== encrypted_flag(hex) ====")[1].strip(), 16)
    private_key_file_name = "private_key.pem"
    cipher_text_file_name = "cipher_text.dat"
    shared_secret_file_name = "shared_secret.dat"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), private_key_file_name), "w") as private_key_file:
        private_key_file.write(private_key)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), cipher_text_file_name), "wb") as cipher_text_file:
        cipher_text_file.write(long_to_bytes(cipher_text))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared.dat"), "wb") as shared_secret_file:
        subprocess.run([
                openssl_path, "pkeyutl", "-decap", 
                "-inkey", os.path.join(os.path.dirname(os.path.abspath(__file__)), private_key_file_name), 
                "-in", os.path.join(os.path.dirname(os.path.abspath(__file__)), cipher_text_file_name), 
                "-out", os.path.join(os.path.dirname(os.path.abspath(__file__)), shared_secret_file_name)
            ], check=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), shared_secret_file_name), "rb") as shared_secret_file:
        shared_secret = shared_secret_file.read()
    cipher = AES.new(shared_secret, AES.MODE_ECB)
    decrypted_flag = unpad(cipher.decrypt(long_to_bytes(encrypted_flag)), 16)
    flag = decrypted_flag.decode()
    return flag

if __name__ == "__main__":
    output_file_name = "output.txt"
    openssl_path = r"C:\\Lab\\OpenSSL-Win64\\bin\\openssl.exe"
    print(solution(output_file_name, openssl_path))
