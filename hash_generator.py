"""
hash_generator.py — Password Security Lab
==========================================
Demonstrates how passwords are converted into fixed-length hash digests.

HOW HASHING WORKS:
  A hash function takes any input (a password) and produces a fixed-length
  string of bytes. The same input always produces the same output, but it is
  computationally infeasible to reverse the process — you cannot get the
  original password back from the hash alone.

  Common algorithms:
    • MD5    — 128-bit digest. Fast but broken; DO NOT use for real passwords.
    • SHA-256 — 256-bit digest. Part of the SHA-2 family; far more secure.

  Modern systems add a random "salt" before hashing to prevent pre-computed
  (rainbow-table) attacks. This lab focuses on unsalted hashes to illustrate
  why weak passwords are still vulnerable even with strong algorithms.

Usage examples:
  python hash_generator.py --password "password123" --algo sha256
  python hash_generator.py --password "letmein" --algo md5
  python hash_generator.py --password "hello" --algo sha256 --show-both
"""

import hashlib
import argparse


# ──────────────────────────────────────────────
# Supported algorithms and their hashlib names
# ──────────────────────────────────────────────
SUPPORTED_ALGORITHMS = {
    "md5":    "md5",
    "sha256": "sha256",
}


def hash_password(password: str, algorithm: str) -> str:
    """
    Hash a plaintext password using the specified algorithm.

    Parameters
    ----------
    password  : The plaintext password string.
    algorithm : One of the keys in SUPPORTED_ALGORITHMS.

    Returns
    -------
    A lowercase hex digest string.
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. "
            f"Choose from: {', '.join(SUPPORTED_ALGORITHMS)}"
        )

    # Encode the password to bytes (UTF-8) — hashlib requires bytes, not str
    password_bytes = password.encode("utf-8")

    # Create a new hash object for the chosen algorithm
    hasher = hashlib.new(SUPPORTED_ALGORITHMS[algorithm], password_bytes)

    # Return the hexadecimal representation of the digest
    return hasher.hexdigest()


def print_hash_info(password: str, algorithm: str) -> None:
    """Pretty-print hash details for a given password and algorithm."""
    digest = hash_password(password, algorithm)
    algo_upper = algorithm.upper()
    digest_bits = len(digest) * 4  # each hex char = 4 bits

    print()
    print("=" * 55)
    print("  Password Hash Generator — Password Security Lab")
    print("=" * 55)
    print(f"  Plaintext  : {password}")
    print(f"  Algorithm  : {algo_upper}  ({digest_bits}-bit digest)")
    print(f"  Hash       : {digest}")
    print("=" * 55)
    print()
    print("  ⚠  NOTE: This hash has NO salt.")
    print("     If the password is common, a dictionary attack")
    print("     can crack it in milliseconds.")
    print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hash_generator.py",
        description=(
            "Generate a hash from a plaintext password.\n"
            "Part of the Password Security Lab — educational use only."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python hash_generator.py --password password123 --algo sha256\n"
            "  python hash_generator.py --password letmein --algo md5\n"
            "  python hash_generator.py --password hello --algo sha256 --show-both\n"
        ),
    )
    parser.add_argument(
        "--password",
        required=True,
        help="The plaintext password to hash.",
    )
    parser.add_argument(
        "--algo",
        required=True,
        choices=list(SUPPORTED_ALGORITHMS.keys()),
        metavar="ALGORITHM",
        help=f"Hashing algorithm to use. Choices: {', '.join(SUPPORTED_ALGORITHMS)}",
    )
    parser.add_argument(
        "--show-both",
        action="store_true",
        help="Also show the hash under the other supported algorithm for comparison.",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()

    print_hash_info(args.password, args.algo)

    if args.show_both:
        other = [a for a in SUPPORTED_ALGORITHMS if a != args.algo][0]
        print(f"  — Comparison ({other.upper()}) —")
        print_hash_info(args.password, other)


if __name__ == "__main__":
    main()