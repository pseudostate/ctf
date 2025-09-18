import os, re

def get_data(file_name: str) -> dict[str, int]:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r", encoding = "UTF-8", errors = "ignore") as f:
        data = f.read()
    return data

def solution(file_name: str) -> str:
    data = get_data(file_name)
    chunks = {int(index): hex_value for index, hex_value in re.compile(r"X-Flag-Chunk-(\d{4}):\s*([a-fA-F0-9]+)").findall(data)}
    full_hex_value = "".join(chunks[i] for i in sorted(chunks.keys()))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag.png"), "wb") as f:
        f.write(bytes.fromhex(full_hex_value))

if __name__ == "__main__":
    file_name = "network_capture.pcap"
    solution(file_name)
    