"""
examples/demo.py — Password Security Lab
=========================================
A pure-Python walkthrough of the full workflow.
Run from the project root:

    python examples/demo.py
"""

import sys
import os
import hashlib

# Make sure we can import the project modules from the root directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hash_generator import hash_password
from cracker import run_dictionary_attack, print_result

DIVIDER = "=" * 55
WORDLIST = os.path.join(os.path.dirname(__file__), "..", "wordlist.txt")


def section(title: str) -> None:
    print()
    print(DIVIDER)
    print(f"  {title}")
    print(DIVIDER)
    print()


def demo_hash_generation() -> None:
    section("STEP 1 — Generating password hashes")

    samples = [
        ("password123", "sha256"),
        ("letmein",     "md5"),
        ("hello",       "sha256"),
    ]

    for pwd, algo in samples:
        digest = hash_password(pwd, algo)
        print(f"  {algo.upper():8}  |  {pwd:15}  →  {digest}")

    print()
    print("  Observation: the same password always produces the same hash.")
    print("  Different passwords of any length produce fixed-length digests.")


def demo_crack_weak(password: str, algo: str) -> None:
    section(f"STEP 2 — Cracking '{password}' ({algo.upper()})")

    target = hash_password(password, algo)
    print(f"  Target hash: {target}")
    print()

    result = run_dictionary_attack(
        target_hash=target,
        wordlist_path=WORDLIST,
        algorithm=algo,
    )
    print_result(result, target)


def demo_strong_password() -> None:
    section("STEP 3 — Attempting to crack a strong password (should FAIL)")

    strong_pwd = "xK#9mP$2qLzR"
    algo = "sha256"
    target = hash_password(strong_pwd, algo)

    print(f"  Real password : {strong_pwd}")
    print(f"  Target hash   : {target}")
    print()

    result = run_dictionary_attack(
        target_hash=target,
        wordlist_path=WORDLIST,
        algorithm=algo,
    )
    print_result(result, target)

    print("  Lesson: A randomly generated password that does not appear")
    print("  in any wordlist is safe against dictionary attacks.")


def main() -> None:
    print()
    print(DIVIDER)
    print("  Password Security Lab — Python Demo")
    print(DIVIDER)

    demo_hash_generation()
    demo_crack_weak("password123", "sha256")
    demo_crack_weak("letmein", "md5")
    demo_strong_password()

    print()
    print(DIVIDER)
    print("  Demo complete — see README.md for the full write-up.")
    print(DIVIDER)
    print()


if __name__ == "__main__":
    main()