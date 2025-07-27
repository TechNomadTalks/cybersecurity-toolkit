# tools/wifi_sniffer.py

from scapy.all import sniff, Dot11

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            ssid = pkt.info.decode()
            bssid = pkt.addr2
            print(f"[+] SSID: {ssid} | BSSID: {bssid}")

if __name__ == "__main__":
    print("📡 Sniffing WiFi... Press CTRL+C to stop.")
    sniff(iface="wlan0mon", prn=packet_handler)


# 🛠️ Requires:
# sudo airmon-ng start wlan0
# sudo python tools/wifi_sniffer.py
