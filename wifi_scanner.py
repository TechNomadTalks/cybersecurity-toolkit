# wifi_scanner.py

from scapy.all import sniff, Dot11
from utils.printer import info, success

networks = set()

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:  # Beacon frame
            ssid = pkt.info.decode(errors='ignore')
            bssid = pkt.addr2
            if ssid not in networks:
                networks.add(ssid)
                success(f"SSID: {ssid} | BSSID: {bssid}")

def start_scan(interface="wlan0mon"):
    info(f"Starting WiFi scan on {interface}... Press Ctrl+C to stop.")
    sniff(iface=interface, prn=packet_handler, store=0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="WiFi network scanner (Linux only)")
    parser.add_argument("-i", "--interface", default="wlan0mon", help="Monitor mode interface")
    args = parser.parse_args()

    start_scan(args.interface)
