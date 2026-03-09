import hashlib
import argparse
import time
import sys
import os
########################################
SUPPORTED_ALGORITHMS = ["md5", "sha256"]

def hash_candidate(candidate, algorithm):
    return hashlib.new(algorithm, candidate.encode("utf-8")).hexdigest()

def run_attack(target_hash, wordlist_path, algorithm, verbose=False):
    target_hash = target_hash.strip().lower()

    if not os.path.isfile(wordlist_path):
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        sys.exit(1)

    print()
    print("=" * 50)
    print("  Dictionary Attack")
    print("=" * 50)
    print(f"  Target    : {target_hash}")
    print(f"  Algorithm : {algorithm.upper()}")
    print(f"  Wordlist  : {wordlist_path}")
    print("=" * 50)
    print()
    print("  [*] Starting attack...")
    print()

    attempts = 0
    start = time.perf_counter()

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            candidate = line.strip()
            if not candidate:
                continue

            attempts += 1

            if verbose and attempts % 1000 == 0:
                print(f"  [~] Tried {attempts:,} passwords... last: {candidate}")

            if hash_candidate(candidate, algorithm) == target_hash:
                elapsed = time.perf_counter() - start
                return {
                    "found": True,
                    "password": candidate,
                    "attempts": attempts,
                    "elapsed": elapsed,
                }

    elapsed = time.perf_counter() - start
    return {
        "found": False,
        "password": None,
        "attempts": attempts,
        "elapsed": elapsed,
    }

def print_result(result, target_hash):
    print()
    if result["found"]:
        print("  Password cracked!")
        print()
        print(f"  Hash     : {target_hash}")
        print(f"  Password : {result['password']}")
        print(f"  Attempts : {result['attempts']:,}")
        print(f"  Time     : {result['elapsed']:.4f} seconds")
    else:
        print("  Password not found in wordlist.")
        print()
        print(f"  Hash     : {target_hash}")
        print(f"  Attempts : {result['attempts']:,}")
        print(f"  Time     : {result['elapsed']:.4f} seconds")

    print()
    print("=" * 50)
    print()

def build_parser():
    parser = argparse.ArgumentParser(description="Run a dictionary attack against a password hash.")
    parser.add_argument("--hash", required=True, dest="target_hash", help="Hash to crack")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--algo", required=True, choices=SUPPORTED_ALGORITHMS, help="md5 or sha256")
    parser.add_argument("--verbose", action="store_true", help="Print progress every 1000 attempts")
    return parser

def main():
    args = build_parser().parse_args()
    result = run_attack(args.target_hash, args.wordlist, args.algo, args.verbose)
    print_result(result, args.target_hash)
    sys.exit(0 if result["found"] else 1)

if __name__ == "__main__":
    main()