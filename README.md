# Cybersecurity Toolkit (God Tier Edition)

Elite tools for ethical hacking, penetration testing, and recon — built with Python.

## Tools

- 🔍 **Port Scanner Pro**: Fast, threaded, banner grabbing
- 🔓 **Auto Hash Cracker**: Algorithm detection, wordlist cracking
- 🌐 **Ping Sweep+**: OS detection from TTL using raw packets
- 🛡 **Password Strength**: Scoring + HaveIBeenPwned.com leak checks
- 📡 **WiFi Sniffer**: Monitor SSIDs via raw packet scanning (Linux only)

## Install

```bash
pip install scapy requests

## ⚠️ WARNING  
This tool is for **legal, authorized security testing only**.  
Unauthorized use against systems you don’t own is illegal.  


## 🧰 Supported OS by Tool

- **port_scanner.py**  
  ✅ Works on Windows, Linux, and macOS.

- **hash_cracker.py**  
  ✅ Works on Windows, Linux, and macOS.

- **ping_sweep.py**  
  ✅ Works on Windows, Linux, and macOS.  
  Uses native ping commands.

- **password_strength.py**  
  ✅ Works on Windows, Linux, and macOS.  
  Performs local password strength analysis.

- **wifi_scanner.py**  
  ❌ Does **not** work on Windows or macOS.  
  ✅ Linux only (requires `iwlist`).

- **Secret_LinuxOnly.py**  
  ❌ Not compatible with Windows or macOS.  
  ✅ Linux only. A hidden or advanced tool.

- **sql_injection_tester.py**  
  ✅ Works on Windows, Linux, and macOS.  
  Simulated SQL injection tests.

- **exploit_tester.py**  
  ✅ Works on Windows, Linux, and macOS.  
  Tests for LFI and header injection.

- **main.py**  
  ✅ Works on Windows, Linux, and macOS.  
  Acts as the main launcher.

## 📝 Notes

- `wifi_scanner.py` and `Secret_LinuxOnly.py` depend on Linux-only commands and will not work on other systems.
- macOS lacks some Linux networking tools, so some features may require additional setup.
- Windows supports all tools except those requiring Linux-specific utilities.
