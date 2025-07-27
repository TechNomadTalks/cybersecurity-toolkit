import os
from utils.banner import show_banner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")

def run_tool(script_name, args=""):
    full_path = os.path.join(TOOLS_DIR, script_name)
    cmd = f'python "{full_path}" {args}'
    print(f"[INFO] Launching {script_name}...")
    result = os.system(cmd)
    if result != 0:
        print(f"[WARNING] Tool exited with error code: {result}")

def main():
    show_banner()

    while True:
        print("\nSelect a tool to run:")
        print(" [1] Port Scanner Pro")
        print(" [2] Auto Hash Cracker")
        print(" [3] Ping Sweep Advanced")
        print(" [4] Password Strength Check")
        print(" [5] WiFi Scanner (Linux Only)")
        print(" [6] SQL Injection Tester")
        print(" [7] Exploit Tester (Header Injection & LFI)")
        print(" [q] Quit")

        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            run_tool("port_scanner.py")
        elif choice == "2":
            run_tool("hash_cracker.py")
        elif choice == "3":
            run_tool("ping_sweep.py")
        elif choice == "4":
            password = input("Enter password to check: ").strip()
            run_tool("password_strength.py", f'"{password}"')
        elif choice == "5":
            run_tool("Secret_LinuxOnly.py")
        elif choice == "6":
            run_tool("sql_injection_tester.py")
        elif choice == "7":
            # Just run the tool with flags; it will prompt internally
            run_tool("exploit_tester.py", "--header-test --lfi-test")
        elif choice == "q":
            print("[INFO] Exiting...")
            break
        else:
            print("[WARNING] Invalid choice. Try again.")

if __name__ == "__main__":
    main()
