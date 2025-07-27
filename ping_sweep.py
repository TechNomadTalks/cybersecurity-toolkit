from scapy.all import IP, ICMP, sr1, conf
import argparse
import ipaddress
import sys
import time
from concurrent.futures import ThreadPoolExecutor  # Correct import
from tqdm import tqdm

# Disable Scapy warnings
conf.verb = 0

def analyze_ttl(ttl):
    """Guess OS based on TTL value"""
    if ttl <= 64:
        return "Linux/Unix"
    elif ttl <= 128:
        return "Windows"
    else:
        return f"Unknown (TTL: {ttl})"

def ping_host(ip):
    """Ping a single host with timeout and retries"""
    try:
        packet = IP(dst=ip)/ICMP()
        reply = sr1(packet, timeout=1, retry=0, verbose=0)
        if reply:
            return ip, analyze_ttl(reply.ttl)
    except Exception:
        pass
    return None

def validate_subnet(subnet):
    """Validate the subnet format"""
    try:
        if len(subnet.split('.')) == 3:
            test_ip = f"{subnet}.1"
            ipaddress.ip_address(test_ip)
            return True
    except ValueError:
        pass
    return False

def interactive_mode():
    """Interactive user interface"""
    print("\n" + "="*50)
    print("🔥 PING SWEEPER".center(50))
    print("="*50)
    
    while True:
        subnet = input("\nEnter subnet (e.g. 192.168.1): ").strip()
        if validate_subnet(subnet):
            break
        print("❌ Invalid subnet format. Use like: 192.168.1")
    
    while True:
        try:
            start = int(input("Start IP [1]: ").strip() or 1)
            end = int(input(f"End IP [254]: ").strip() or 254)
            if 1 <= start <= end <= 254:
                break
            print("❌ Invalid range. Use 1-254")
        except ValueError:
            print("❌ Please enter numbers")
    
    return subnet, start, end

def sweep(subnet, start, end, threads=50):
    """Multi-threaded ping sweep with progress bar"""
    active_hosts = []
    ips = [f"{subnet}.{i}" for i in range(start, end+1)]
    
    print(f"\n🔍 Scanning {len(ips)} hosts ({subnet}.{start}-{end})...")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(ping_host, ip): ip for ip in ips}
        
        for future in tqdm(
            concurrent.futures.as_completed(futures),  # Fixed reference
            total=len(ips),
            desc="Scanning",
            unit="host"
        ):
            result = future.result()
            if result:
                active_hosts.append(result)
                print(f"\n[+] {result[0]} is up | OS: {result[1]}")
    
    print(f"\n✅ Scan complete. Found {len(active_hosts)} active hosts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Ping Sweeper")
    parser.add_argument("-s", "--subnet", help="Subnet (e.g. 192.168.1)")
    parser.add_argument("--start", type=int, help="Starting IP (1-254)")
    parser.add_argument("--end", type=int, help="Ending IP (1-254)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Thread count [50]")
    
    args = parser.parse_args()
    
    # Interactive mode if no args
    if not args.subnet:
        subnet, start, end = interactive_mode()
    else:
        subnet = args.subnet
        start = args.start if args.start else 1
        end = args.end if args.end else 254
        
        if not validate_subnet(subnet):
            print("❌ Invalid subnet format. Use like: 192.168.1")
            sys.exit(1)
        
        if not (1 <= start <= end <= 254):
            print("❌ Invalid IP range. Use 1-254")
            sys.exit(1)
    
    sweep(subnet, start, end, args.threads)