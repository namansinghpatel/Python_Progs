#=========================================login_system()===============================================================
from getpass import getpass
import base64


# 🔐 Simple encryption (for learning)
def encrypt(password):
    return base64.b64encode(password.encode()).decode()


def decrypt(encoded):
    return base64.b64decode(encoded.encode()).decode()


# 🔐 Stored credentials (encrypted password)
USERNAME = "admin"
ENCRYPTED_PASSWORD = encrypt("1234")


def login_system_manual():
    attempts = 0

    while attempts < 3:
        user = input("User: ")
        pwd = getpass("Pass: ")   # 🔥 hides password

        if user == USERNAME and pwd == decrypt(ENCRYPTED_PASSWORD):
            print("Login success")
            return
        else:
            attempts += 1
            print("Login failed")
            print(f"Attempt {attempts} of 3 failed")

    print("Too many failed attempts. Access denied.")


def login_system_auto(test_cases):
    for i, test in enumerate(test_cases, 1):
        print("\n" + "=" * 20)
        print(f"Test Case {i}")

        attempts = 0
        success = False

        for user, pwd in test:
            if attempts >= 3:
                break

            print(f"Trying: {user} / {pwd}")

            if user == USERNAME and pwd == decrypt(ENCRYPTED_PASSWORD):
                print("Login success")
                success = True
                break
            else:
                attempts += 1
                print("Login failed")

        if not success:
            print("Too many failed attempts. Access denied.")


# 🔥 Test cases
test_cases = [
    [("admin", "1234")],
    [("admin", "wrong"), ("admin", "1234")],
    [("a", "b"), ("c", "d"), ("admin", "1234")],
    [("a", "b"), ("c", "d"), ("e", "f")],
]


def login_system():
    # 🎯 MENU
    while True:
        print("\n==== Login System ====")
        print("1. Manual Login")
        print("2. Run All Test Cases")
        print("3. Show Encrypted Password")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            login_system_manual()

        elif choice == "2":
            login_system_auto(test_cases)

        elif choice == "3":
            print("Encrypted password:", ENCRYPTED_PASSWORD)
            print("Decrypted password:", decrypt(ENCRYPTED_PASSWORD))

        elif choice == "0":
            break

        else:
            print("Invalid choice")

#=========================================encryption_lab()===============================================================
import hashlib
    
DEBUG = True

def log(msg):
    if DEBUG:
        print("[DEBUG]", msg)


# 🔐 1️⃣ Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            new_char = chr((ord(ch) + shift - 97) % 26 + 97)
            log(f"{ch} -> {new_char}")
            result += new_char
        else:
            result += ch
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# 🔐 2️⃣ XOR Encryption
def xor_encrypt(text, key):
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(ord(text[i]) ^ ord(key[i % len(key)]))
        log(f"{text[i]} -> {encrypted[-1]}")
    return base64.b64encode(encrypted.encode()).decode()


def xor_decrypt(encoded_text, key):
    decoded = base64.b64decode(encoded_text).decode()
    decrypted = ""

    for i in range(len(decoded)):
        decrypted += chr(ord(decoded[i]) ^ ord(key[i % len(key)]))
        log(f"{decoded[i]} -> {decrypted[-1]}")

    return decrypted


# 🔐 3️⃣ SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(input_pwd, stored_hash):
    return hash_password(input_pwd) == stored_hash


# =========================
# 🧪 TEST CASES
# =========================

def test_caesar():
    print("\n[TEST] Caesar Cipher")

    text = "hello"
    shift = 2

    enc = caesar_encrypt(text, shift)
    dec = caesar_decrypt(enc, shift)

    print("Encrypted:", enc)
    print("Decrypted:", dec)

    if dec == text:
        print("PASS ✅")
    else:
        print("FAIL ❌")


def test_xor():
    print("\n[TEST] XOR Encryption")

    text = "hello"
    key = "Naman@123"

    enc = xor_encrypt(text, key)
    dec = xor_decrypt(enc, key)

    print("Encrypted:", enc)
    print("Decrypted:", dec)

    if dec == text:
        print("PASS ✅")
    else:
        print("FAIL ❌")


def test_hash():
    print("\n[TEST] SHA-256")

    pwd = "hello"
    hashed = hash_password(pwd)

    result = verify_password("hello", hashed)

    print("Hash:", hashed)

    if result:
        print("PASS ✅")
    else:
        print("FAIL ❌")


def run_all_tests():
    test_caesar()
    test_xor()
    test_hash()


# =========================
# 🎯 MENU
# =========================
def encryption_lab():

    while True:
        print("\n==== Encryption Lab ====")
        print("1. Caesar Cipher (Manual)")
        print("2. XOR Encryption (Manual)")
        print("3. SHA-256 (Manual)")
        print("4. Run All Tests")
        print("5. Toggle Debug Logs")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            text = input("Enter text: ")
            shift = int(input("Enter shift: "))

            enc = caesar_encrypt(text, shift)
            print("Encrypted:", enc)

            dec = caesar_decrypt(enc, shift)
            print("Decrypted:", dec)

        elif choice == "2":
            text = input("Enter text: ")
            key = input("Enter key: ")

            enc = xor_encrypt(text, key)
            print("Encrypted:", enc)

            dec = xor_decrypt(enc, key)
            print("Decrypted:", dec)

        elif choice == "3":
            pwd = input("Enter password: ")

            hashed = hash_password(pwd)
            print("Hash:", hashed)

            test = input("Re-enter password: ")

            if verify_password(test, hashed):
                print("MATCH ✅")
            else:
                print("NOT MATCH ❌")

        elif choice == "4":
            run_all_tests()

        elif choice == "5":
            DEBUG = not DEBUG
            print("DEBUG =", DEBUG)

        elif choice == "0":
            break

        else:
            print("Invalid choice")

#==============================================string_compression()========================================================

def string_compression():

    import time

    print("===== String Compression ====")

    s = "aaabbc"
    result = ""
    count = 1

    print(f"compressing string {s}.......")
    time.sleep(3)

    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            count += 1
        else:
            result += s[i] + str(count)
            count = 1

    # ✅ handle last group
    result += s[-1] + str(count)

    print("compressed =", result)

#============================================frequency_count============================================================
def frequency_count():

    import time 

    print("===== Frequency Count =====")
    nums = [1,2,2,3,3,3]
    freq = {}
    print("counting frequency of", nums)
    time.sleep(2)

    for n in nums:
        if n in freq:
            freq[n] += 1
        else:
            freq[n] = 1

    print(freq)

#=========================================================================================================================



if __name__ == "__main__":
    #login_system()
    #encryption_lab()
    #string_compression()
    frequency_count()
    