# 🔐 Password Security Lab

> **Educational cybersecurity project** demonstrating password hashing, dictionary attacks, and why weak passwords are dangerous — built with pure Python.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Topic](https://img.shields.io/badge/Topic-Cybersecurity-red)
![Status](https://img.shields.io/badge/Status-Educational-yellow)

---

## 📌 Table of Contents

- [Overview](#overview)
- [What Is Password Hashing?](#what-is-password-hashing)
- [What Is a Dictionary Attack?](#what-is-a-dictionary-attack)
- [Why Weak Passwords Are Dangerous](#why-weak-passwords-are-dangerous)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
  - [Generate a Hash](#generate-a-hash)
  - [Crack a Hash](#crack-a-hash)
  - [Run the Full Demo](#run-the-full-demo)
- [Example Output](#example-output)
- [Key Lessons](#key-lessons)
- [Upload to GitHub](#upload-to-github)
- [Disclaimer](#disclaimer)

---

## Overview

**Password Security Lab** is a command-line Python project designed to teach core password-security concepts by letting you:

1. **Hash** a password using MD5 or SHA-256.
2. **Attack** that hash with a wordlist (dictionary attack).
3. **Observe** how quickly a weak password is cracked — and why a strong one resists the attack.

This project is intended for students, cybersecurity beginners, and anyone building a portfolio who wants to demonstrate a practical understanding of hashing and attack techniques.

---

## What Is Password Hashing?

When you create an account on a website, your password is (ideally) never stored as plaintext. Instead, the system runs it through a **hash function** — a one-way mathematical operation that converts any input into a fixed-length string of characters called a *digest*.

```
plaintext  →  hash function  →  digest (hex string)
"password" →  SHA-256        →  5e884898da28047151...
```

Key properties of a good hash function:

| Property | Meaning |
|---|---|
| **Deterministic** | Same input → same output, every time |
| **One-way** | You cannot reverse a digest to get the password |
| **Avalanche effect** | Changing one character changes the entire digest |
| **Fixed length** | Output length is always the same, regardless of input |

### MD5 vs SHA-256

| Algorithm | Digest size | Speed | Security |
|---|---|---|---|
| MD5 | 128-bit (32 hex chars) | Very fast | ❌ Broken — collision attacks exist |
| SHA-256 | 256-bit (64 hex chars) | Fast | ✅ Secure (but not ideal for passwords) |

> **Note:** For real-world password storage, purpose-built algorithms like **bcrypt**, **scrypt**, or **Argon2** are preferred because they are intentionally slow and support salting. This lab uses MD5/SHA-256 to keep the focus on the attack concept.

---

## What Is a Dictionary Attack?

A **dictionary attack** (also called a wordlist attack) works like this:

```
for each candidate in wordlist:
    if hash(candidate) == target_hash:
        password found!  ✅
```

1. The attacker obtains a hash — perhaps from a leaked database.
2. They take a pre-built list of common passwords (the *wordlist*).
3. Each candidate is hashed with the same algorithm as the target.
4. If the hashes match, the plaintext password is recovered.

This is effective because:
- Hashing is **deterministic** — the same password always produces the same hash.
- Without a unique **salt** per user, one computation covers every account sharing that password.
- Millions of people use passwords like `password123`, `letmein`, or `qwerty`.

---

## Why Weak Passwords Are Dangerous

Even with a **strong algorithm** like SHA-256, a weak password can be cracked in **milliseconds**:

```
SHA-256("password") → 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

This hash appears in every major rainbow table and wordlist. The moment an attacker sees it, they know the password.

### The math of brute force

| Password type | Example | Possible combinations | Time to brute force* |
|---|---|---|---|
| 6-digit PIN | `123456` | 1 000 000 | < 1 second |
| 8-char lowercase | `password` | 208 billion | Minutes |
| 12-char mixed | `P@ssw0rd!2#` | 475 quadrillion | Days–months |
| 16-char random | `xK#9mP$2qLzR!8@v` | 10^30+ | Centuries |

\* Estimates for a modern GPU cracking MD5 at ~10 billion hashes/second.

**Best practices:**
- Use a password manager to generate long, random passwords.
- Never reuse passwords across sites.
- Enable multi-factor authentication (MFA).
- Developers: hash with **bcrypt/Argon2** + a unique salt per user.

---

## Project Structure

```
password-security-lab/
│
├── hash_generator.py   # CLI tool — generate hashes from plaintext passwords
├── cracker.py          # CLI tool — run a dictionary attack against a hash
├── wordlist.txt        # Sample wordlist of 100+ common passwords
├── requirements.txt    # Dependencies (standard library only)
├── README.md           # This file
│
└── examples/
    ├── demo.py         # Pure-Python end-to-end walkthrough
    └── demo.sh         # Bash end-to-end walkthrough (Linux/macOS)
```

---

## Setup & Installation

### Prerequisites

- Python 3.8 or newer
- No third-party packages required (standard library only)

### Clone the repository

```bash
git clone https://github.com/fatlum1300/password-security-lab.git
cd password-security-lab
```

### (Optional) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate.bat     # Windows
```

### Verify everything is in place

```bash
python --version
ls                             # or dir on Windows
```

You should see `hash_generator.py`, `cracker.py`, and `wordlist.txt`.

---

## Usage

### Generate a Hash

```bash
python hash_generator.py --password <plaintext> --algo <md5|sha256>
```

| Flag | Required | Description |
|---|---|---|
| `--password` | ✅ | The plaintext password to hash |
| `--algo` | ✅ | Algorithm: `md5` or `sha256` |
| `--show-both` | ❌ | Also display the hash under the other algorithm |

**Examples:**

```bash
# SHA-256 hash of "password123"
python hash_generator.py --password password123 --algo sha256

# MD5 hash of "letmein"
python hash_generator.py --password letmein --algo md5

# Show both algorithms side by side
python hash_generator.py --password hello --algo sha256 --show-both
```

---

### Crack a Hash

```bash
python cracker.py --hash <hex_digest> --wordlist <file> --algo <md5|sha256>
```

| Flag | Required | Description |
|---|---|---|
| `--hash` | ✅ | The target hex digest to crack |
| `--wordlist` | ✅ | Path to wordlist file |
| `--algo` | ✅ | Algorithm used to create the hash |
| `--verbose` | ❌ | Print progress every 1 000 attempts |

**Examples:**

```bash
# Crack a SHA-256 hash
python cracker.py \
  --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \
  --wordlist wordlist.txt \
  --algo sha256

# Crack an MD5 hash
python cracker.py \
  --hash 0d107d09f5bbe40cade3de5c71e9e9b7 \
  --wordlist wordlist.txt \
  --algo md5
```

---

### Run the Full Demo

**Python (all platforms):**
```bash
python examples/demo.py
```

**Bash (Linux / macOS):**
```bash
chmod +x examples/demo.sh
./examples/demo.sh
```

---

## Example Output

**Generating a hash:**
```
=======================================================
  Password Hash Generator — Password Security Lab
=======================================================
  Plaintext  : password123
  Algorithm  : SHA256  (256-bit digest)
  Hash       : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
=======================================================

  ⚠  NOTE: This hash has NO salt.
     If the password is common, a dictionary attack
     can crack it in milliseconds.
```

**Cracking a hash:**
```
=======================================================
  Dictionary Attack — Password Security Lab
=======================================================
  Target hash : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  Algorithm   : SHA256
  Wordlist    : wordlist.txt
=======================================================

  [*] Starting attack …

  ✅  PASSWORD CRACKED!

  Hash      : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  Password  : password123
  Attempts  : 14
  Time      : 0.0003 seconds

  ⚠  This password was found in a wordlist.
     It should NEVER be used in a real system.
```

**Strong password — attack fails:**
```
  ❌  Password NOT found in wordlist.

  Hash      : 3d8b2a4c9e1f7062…
  Attempts  : 104
  Time      : 0.0021 seconds

  The password may be strong, or it may simply be absent
  from this wordlist. A larger wordlist or a brute-force
  attack could still crack it given enough time.
```

---

## Key Lessons

| Concept | Takeaway |
|---|---|
| Hashing is one-way | You cannot decrypt a hash — only brute-force or use a wordlist |
| Algorithm strength ≠ password strength | SHA-256 on `password` is still instantly crackable |
| Salting matters | A unique random salt per user defeats rainbow tables |
| Common passwords are pre-computed | Major wordlists contain billions of entries |
| Password length > complexity | `correcthorsebatterystaple` beats `P@ss1!` |

---

## Upload to GitHub

Follow these steps to publish this project to GitHub under the account **fatlum1300**:

### 1. Create the repository on GitHub

1. Go to [https://github.com/new](https://github.com/new)
2. Sign in as **fatlum1300** (fa31647@seeu.edu.mk)
3. Repository name: `password-security-lab`
4. Description: `Educational Python project demonstrating password hashing and dictionary attacks`
5. Set visibility: **Public**
6. **Do not** initialise with a README (you already have one)
7. Click **Create repository**

### 2. Initialise git locally

```bash
cd password-security-lab

git init
git add .
git commit -m "Initial commit: Password Security Lab"
```

### 3. Configure your identity (first time only)

```bash
git config --global user.name  "fatlum1300"
git config --global user.email "fa31647@seeu.edu.mk"
```

### 4. Push to GitHub

```bash
git remote add origin https://github.com/fatlum1300/password-security-lab.git
git branch -M main
git push -u origin main
```

### 5. Add topics for discoverability

On the GitHub repository page, click the gear icon next to **About** and add topics:
`cybersecurity`, `python`, `hashing`, `password-security`, `dictionary-attack`, `ethical-hacking`, `portfolio`

---

## Disclaimer

> This project is created **strictly for educational purposes**.
> All techniques demonstrated are intended to teach password security awareness.
> Do **not** use these tools against systems, accounts, or hashes that you do not own or have explicit permission to test.
> Unauthorised access to computer systems is illegal and unethical.

---

*Built by [fatlum1300](https://github.com/fatlum1300) · Password Security Lab · MIT License*