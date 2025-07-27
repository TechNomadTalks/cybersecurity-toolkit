import socket
import argparse
import concurrent.futures

# Constants
DEFAULT_TARGET = "scanme.nmap.org"  # Test-friendly target
DEFAULT_PORTS = "20-80"            # Safe, limited range
SOCKET_TIMEOUT = 0.5               # Seconds

def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect((ip, port))
        try:
            banner = sock.recv(1024).decode().strip()
        except:
            banner = "No banner"
        return port, banner
    except:
        return None
    finally:
        sock.close()

def scan(ip, start, end):
    print(f"\n🔍 Scanning {ip} (ports {start}-{end})...\n")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, p) for p in range(start, end+1)]
        for f in concurrent.futures.as_completed(futures):
            result = f.result()
            if result:
                port, banner = result
                results.append((port, banner))
                print(f"[+] Port {port} open - Banner: {banner}")
    
    print(f"\n✅ Scan completed. {len(results)} ports open.")
    return results

def get_user_input():
    """Interactive mode prompt"""
    print("\n" + "="*40)
    print("PYTHON PORT SCANNER (Interactive Mode)")
    print("="*40)
    
    target = input(f"Target IP/Domain [default: {DEFAULT_TARGET}]: ").strip()
    ports = input(f"Port Range [default: {DEFAULT_PORTS}]: ").strip()
    
    return target or DEFAULT_TARGET, ports or DEFAULT_PORTS

if __name__ == "__main__":
    # Argument parsing (will use defaults if running interactively)
    parser = argparse.ArgumentParser(description="Python Port Scanner with Threading")
    parser.add_argument("-t", "--target", help=f"Target IP/domain (default: {DEFAULT_TARGET})")
    parser.add_argument("-p", "--ports", help=f"Port range (e.g. 80 or 20-443, default: {DEFAULT_PORTS})")
    args = parser.parse_args()

    # Interactive mode if no args provided
    if not args.target or not args.ports:
        args.target, args.ports = get_user_input()

    # Resolve target
    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"❌ Could not resolve hostname: {args.target}")
        exit(1)

    # Port range handling
    try:
        if "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
        else:
            start = end = int(args.ports)  # Single port mode
        
        if start > end:
            print("❌ Invalid port range (start > end)")
            exit(1)
            
    except ValueError:
        print("❌ Invalid port format. Use like: 80 or 20-443")
        exit(1)

    scan(ip, start, end)