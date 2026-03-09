"""
cracker.py — Password Security Lab
====================================
Demonstrates a dictionary (wordlist) attack against unsalted password hashes.

HOW A DICTIONARY ATTACK WORKS:
  1. The attacker obtains a hash (e.g., stolen from a database breach).
  2. They take a large list of candidate passwords (the "wordlist").
  3. Each candidate is hashed with the same algorithm used to store the password.
  4. If the computed hash matches the target hash, the password is found.

  This works because:
    • Hashing is deterministic  — same input → same output, always.
    • Many users pick common, guessable passwords.
    • Without a unique salt per user, one pre-computed list covers everyone
      who shares a password.

  Key takeaway: A strong algorithm (SHA-256) does NOT protect a weak password.

Usage examples:
  python cracker.py --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \\
                    --wordlist wordlist.txt --algo sha256

  python cracker.py --hash 5f4dcc3b5aa765d61d8327deb882cf99 \\
                    --wordlist wordlist.txt --algo md5
"""

import hashlib
import argparse
import time
import sys
import os


# ──────────────────────────────────────────────
# Supported algorithms (mirror of hash_generator)
# ──────────────────────────────────────────────
SUPPORTED_ALGORITHMS = {
    "md5":    "md5",
    "sha256": "sha256",
}


def hash_candidate(candidate: str, algorithm: str) -> str:
    """
    Hash a single candidate password and return its hex digest.

    This is called once per wordlist entry during the attack loop —
    performance here directly affects cracking speed.
    """
    return hashlib.new(
        SUPPORTED_ALGORITHMS[algorithm],
        candidate.encode("utf-8"),
    ).hexdigest()


def run_dictionary_attack(
    target_hash: str,
    wordlist_path: str,
    algorithm: str,
    verbose: bool = False,
) -> dict:
    """
    Attempt to find the plaintext password behind *target_hash*.

    Parameters
    ----------
    target_hash   : The hex digest we are trying to reverse.
    wordlist_path : Path to a plaintext file with one password per line.
    algorithm     : The hashing algorithm used to create target_hash.
    verbose       : Print progress every 1 000 attempts if True.

    Returns
    -------
    A result dict with keys:
      found        (bool)
      password     (str | None)
      attempts     (int)
      elapsed_sec  (float)
    """
    # Normalise the target hash to lowercase for reliable comparison
    target_hash = target_hash.strip().lower()

    if not os.path.isfile(wordlist_path):
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        sys.exit(1)

    print()
    print("=" * 55)
    print("  Dictionary Attack — Password Security Lab")
    print("=" * 55)
    print(f"  Target hash : {target_hash}")
    print(f"  Algorithm   : {algorithm.upper()}")
    print(f"  Wordlist    : {wordlist_path}")
    print("=" * 55)
    print()
    print("  [*] Starting attack …")
    print()

    attempts = 0
    start_time = time.perf_counter()

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as fh:
        for raw_line in fh:
            # Strip newline / surrounding whitespace
            candidate = raw_line.strip()

            # Skip blank lines
            if not candidate:
                continue

            attempts += 1

            # ── Core of the attack: hash the candidate and compare ──
            candidate_hash = hash_candidate(candidate, algorithm)

            if verbose and attempts % 1_000 == 0:
                print(f"  [~] Tried {attempts:,} passwords …  last: {candidate}")

            if candidate_hash == target_hash:
                elapsed = time.perf_counter() - start_time
                return {
                    "found":       True,
                    "password":    candidate,
                    "attempts":    attempts,
                    "elapsed_sec": elapsed,
                }

    elapsed = time.perf_counter() - start_time
    return {
        "found":       False,
        "password":    None,
        "attempts":    attempts,
        "elapsed_sec": elapsed,
    }


def print_result(result: dict, target_hash: str) -> None:
    """Display the attack outcome in a formatted block."""
    print()
    if result["found"]:
        print("  ✅  PASSWORD CRACKED!")
        print()
        print(f"  Hash      : {target_hash}")
        print(f"  Password  : {result['password']}")
        print(f"  Attempts  : {result['attempts']:,}")
        print(f"  Time      : {result['elapsed_sec']:.4f} seconds")
        print()
        print("  ⚠  This password was found in a wordlist.")
        print("     It should NEVER be used in a real system.")
    else:
        print("  ❌  Password NOT found in wordlist.")
        print()
        print(f"  Hash      : {target_hash}")
        print(f"  Attempts  : {result['attempts']:,}")
        print(f"  Time      : {result['elapsed_sec']:.4f} seconds")
        print()
        print("  The password may be strong, or it may simply be absent")
        print("  from this wordlist. A larger wordlist or a brute-force")
        print("  attack could still crack it given enough time.")

    print()
    print("=" * 55)
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cracker.py",
        description=(
            "Run a dictionary attack against a password hash.\n"
            "Part of the Password Security Lab — educational use only."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cracker.py \\\n"
            "    --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \\\n"
            "    --wordlist wordlist.txt --algo sha256\n\n"
            "  python cracker.py \\\n"
            "    --hash 5f4dcc3b5aa765d61d8327deb882cf99 \\\n"
            "    --wordlist wordlist.txt --algo md5\n"
        ),
    )
    parser.add_argument(
        "--hash",
        required=True,
        dest="target_hash",
        help="The hex digest to crack.",
    )
    parser.add_argument(
        "--wordlist",
        required=True,
        help="Path to the wordlist file (one password per line).",
    )
    parser.add_argument(
        "--algo",
        required=True,
        choices=list(SUPPORTED_ALGORITHMS.keys()),
        metavar="ALGORITHM",
        help=f"Algorithm used to create the hash. Choices: {', '.join(SUPPORTED_ALGORITHMS)}",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress every 1 000 attempts.",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()

    result = run_dictionary_attack(
        target_hash=args.target_hash,
        wordlist_path=args.wordlist,
        algorithm=args.algo,
        verbose=args.verbose,
    )

    print_result(result, args.target_hash)

    # Exit with code 0 if cracked, 1 if not — useful for scripting
    sys.exit(0 if result["found"] else 1)


if __name__ == "__main__":
    main()