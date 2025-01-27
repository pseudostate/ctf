import os

def solution(file_name: str) -> None:
    read_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(read_file_path, "r") as f:
        print(bytes(b ^ 0x1a for b in bytes.fromhex(f.read().strip())).decode())

if __name__=="__main__":
    file_name = "flag.txt"
    solution(file_name)
    