import hashlib
import os

def hashGen(email, password):
    
    salt = os.urandom(32)
    emailHash = email
    passwordHash = password

    key = hashlib.pbkdf2_hmac(
        "sha256",
        emailHash.encode("utf-8"),
        passwordHash.encode("utf-8"),
        salt,
        100000,
        dklen = 128
    )

    print(key)