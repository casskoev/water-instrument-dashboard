"""
Generate a bcrypt password hash to paste into credentials.yaml.

Usage:
    python scripts/hash_password.py
    (you will be prompted for a password; it will not echo)

Or:
    python scripts/hash_password.py "their_password_here"

Paste the printed hash into the user's `password:` field in credentials.yaml.
"""

import getpass
import sys

import bcrypt


def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def main() -> None:
    if len(sys.argv) > 1:
        plain = sys.argv[1]
    else:
        plain = getpass.getpass("Password to hash: ")
        confirm = getpass.getpass("Confirm: ")
        if plain != confirm:
            print("Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    if not plain:
        print("Empty password not allowed.", file=sys.stderr)
        sys.exit(1)

    print(hash_password(plain))


if __name__ == "__main__":
    main()
