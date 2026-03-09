import hashlib
import argparse

SUPPORTED_ALGORITHMS = ["md5", "sha256"]

def hash_password(password, algorithm):
    password_bytes = password.encode("utf-8")
    hasher = hashlib.new(algorithm, password_bytes)
    return hasher.hexdigest()

def print_result(password, algorithm, digest):
    print()
    print("=" * 50)
    print("  Password Hash Generator")
    print("=" * 50)
    print(f"  Plaintext : {password}")
    print(f"  Algorithm : {algorithm.upper()}")
    print(f"  Hash      : {digest}")
    print("=" * 50)
    print()

def build_parser():
    parser = argparse.ArgumentParser(description="Generate a hash from a plaintext password.")
    parser.add_argument("--password", required=True, help="Password to hash")
    parser.add_argument("--algo", required=True, choices=SUPPORTED_ALGORITHMS, help="md5 or sha256")
    parser.add_argument("--show-both", action="store_true", help="Show hash under both algorithms")
    return parser

def main():
    args = build_parser().parse_args()
    digest = hash_password(args.password, args.algo)
    print_result(args.password, args.algo, digest)

    if args.show_both:
        other = [a for a in SUPPORTED_ALGORITHMS if a != args.algo][0]
        other_digest = hash_password(args.password, other)
        print_result(args.password, other, other_digest)

if __name__ == "__main__":
    main()