import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hash_generator import hash_password
from cracker import run_attack, print_result

WORDLIST = os.path.join(os.path.dirname(__file__), "..", "wordlist.txt")
DIVIDER = "=" * 50

def section(title):
    print()
    print(DIVIDER)
    print(f"  {title}")
    print(DIVIDER)
    print()

def main():
    print()
    print(DIVIDER)
    print("  Password Security Lab - Demo")
    print(DIVIDER)

    section("STEP 1 - Generating hashes")
    for pwd, algo in [("password123", "sha256"), ("letmein", "md5"), ("hello", "sha256")]:
        digest = hash_password(pwd, algo)
        print(f"  {algo.upper():8}  {pwd:15}  ->  {digest}")

    section("STEP 2 - Cracking 'password123' with SHA-256")
    target = hash_password("password123", "sha256")
    result = run_attack(target, WORDLIST, "sha256")
    print_result(result, target)

    section("STEP 3 - Cracking 'letmein' with MD5")
    target = hash_password("letmein", "md5")
    result = run_attack(target, WORDLIST, "md5")
    print_result(result, target)

    section("STEP 4 - Strong password (should fail)")
    target = hash_password("xK#9mP$2qLzR", "sha256")
    result = run_attack(target, WORDLIST, "sha256")
    print_result(result, target)

    print(DIVIDER)
    print("  Demo complete.")
    print(DIVIDER)
    print()

if __name__ == "__main__":
    main()