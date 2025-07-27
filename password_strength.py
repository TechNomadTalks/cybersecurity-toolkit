import argparse
import re

# Sample local breach list (for demo)
BREACHED_PASSWORDS = {"123456", "password", "admin", "qwerty", "letmein", "focus"}

def check_password_strength(password):
    weaknesses = []

    if len(password) < 8:
        weaknesses.append("Too short")
    if not re.search(r"[a-z]", password):
        weaknesses.append("Missing lowercase")
    if not re.search(r"[A-Z]", password):
        weaknesses.append("Missing uppercase")
    if not re.search(r"[0-9]", password):
        weaknesses.append("Missing digits")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        weaknesses.append("Missing special char")

    return weaknesses

def check_breached(password):
    return password.lower() in BREACHED_PASSWORDS

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("password", help="Password to check")
    args = parser.parse_args()

    print("Analyzing password strength...\n")

    issues = check_password_strength(args.password)
    if issues:
        print("⚠️ Weaknesses:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("✅ Strong password!")

    if check_breached(args.password):
        print("⚠️ Found in breached database!")

    # Always show this notice
    print("\nThis result is based on a local test list and may not reflect real-world breach data.")
