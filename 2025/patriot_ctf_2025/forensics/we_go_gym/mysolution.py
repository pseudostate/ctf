from scapy.all import rdpcap, PacketList, Raw, IP

def get_data(pcap_file: str) -> PacketList:
    return rdpcap(pcap_file)

def solution(pcap_file: str) -> str:
    flag = ""
    for packet in get_data(pcap_file):
        try:
            payload = packet[Raw].load.decode()
            if "User-Agent" in payload and "CURL" in payload:
                flag += chr(packet[IP].ttl)
        except:
            continue
    return flag

if __name__ == "__main__":
    pcap_file = "wegogym.pcap"
    print(solution(pcap_file))
    