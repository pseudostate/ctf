import os

def solution(file_name: str) -> None:
    read_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    write_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"decryption_{file_name}")
    with open(read_file_path, "rb") as f:
        data = f.read()
        with open(write_file_path, "wb") as f:
            f.write(bytes(b ^ 0x30 for b in data))

if __name__=="__main__":
    file_name = "flag.jpeg"
    solution(file_name)
    