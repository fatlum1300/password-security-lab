# Password Security Lab

I built this project to better understand how password hashing works and why weak passwords are so easy to crack. I was curious about what actually happens when a database gets breached and decided to build a tool that simulates it.

The idea is simple — you take a password, hash it, and then try to crack that hash using a wordlist. Seeing it work in real time made everything click for me way more than just reading about it.

---

## What I built

- `hash_generator.py` — takes any password and hashes it using MD5 or SHA-256
- `cracker.py` — takes a hash and tries to crack it by going through a wordlist
- `wordlist.txt` — a list of common passwords used for the attack
- `examples/demo.py` — runs the whole thing end to end so you can see it all at once

---

## Why I made this

I was learning about cybersecurity and kept reading about data breaches where millions of passwords get leaked. I wanted to understand how attackers actually go from a stolen hash back to a real password. Building this made it obvious — if your password is common, it doesn't matter what algorithm was used to hash it. It will be cracked in seconds.

The part that surprised me most was realizing that SHA-256 is used in Bitcoin and by major banks, but it still can't protect a weak password. The algorithm isn't the problem — the password is.

---

## How it works

When you create an account on a website, your password gets run through a hash function before being saved. The website never stores your actual password, just the hash. When you log in, it hashes what you typed and compares it to the stored hash.

The problem is that hashing is deterministic — the same password always produces the same hash. So if an attacker steals a database full of hashes, they can just hash every word in a wordlist and compare. If anything matches, they have your password.

That is exactly what `cracker.py` does.

---

## Setup

No installs needed. Just Python 3.8 or above.

Clone the repo:
```
git clone https://github.com/fatlum1300/password-security-lab.git
cd password-security-lab
```

---

## Usage

**Generate a hash:**
```
python hash_generator.py --password fatlum1300 --algo sha256
```

**Crack a hash:**
```
python cracker.py --hash <paste hash here> --wordlist wordlist.txt --algo sha256
```

**Run the full demo:**
```
python examples/demo.py
```

---

## Example output

```
==================================================
  Dictionary Attack
==================================================
  Target    : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  Algorithm : SHA256
  Wordlist  : wordlist.txt
==================================================

  [*] Starting attack...

  Password cracked!

  Hash     : ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
  Password : password123
  Attempts : 50
  Time     : 0.0003 seconds
```

---

## What I learned

- Hashing is one way — you can never reverse a hash back to the original password
- The same password always produces the same hash which is exactly what makes dictionary attacks possible
- A strong algorithm like SHA-256 means nothing if the password itself is weak
- The only thing that actually protects a password is making it long and random enough that it will never appear in any wordlist
- Real systems should use bcrypt or Argon2 with a unique salt per user — these are designed specifically for passwords and are intentionally slow to make cracking impractical

---

## Disclaimer

Built for learning purposes. Only run this against hashes you created yourself.