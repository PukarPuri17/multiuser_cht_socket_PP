# auth_db.py
import sqlite3
import os
import hashlib
import hmac

DB_PATH = "chat.db"

def init_db():
    """Create database + users table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                pw_hash  BLOB NOT NULL,
                salt     BLOB NOT NULL
            )
        """)
        conn.commit()

def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120_000
    )

def register_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "Username and password cannot be empty."

    salt = os.urandom(16)
    pw_hash = _hash_password(password, salt)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users(username, pw_hash, salt) VALUES (?, ?, ?)",
                (username, pw_hash, salt)
            )
            conn.commit()
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username already exists."

def login_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT pw_hash, salt FROM users WHERE username=?",
            (username,)
        ).fetchone()

    if not row:
        return False, "User not found."

    stored_hash, salt = row
    attempt_hash = _hash_password(password, salt)

    if hmac.compare_digest(stored_hash, attempt_hash):
        return True, "Login successful."
    return False, "Incorrect password."