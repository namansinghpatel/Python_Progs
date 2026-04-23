# =========================================login_system()===============================================================
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
        pwd = getpass("Pass: ")  # 🔥 hides password

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


# =========================================encryption_lab()===============================================================
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


# ==============================================string_compression()========================================================


def string_compression():

    import time

    print("===== String Compression ====")

    s = "aaabbc"
    result = ""
    count = 1

    print(f"compressing string {s}.......")
    time.sleep(3)

    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            count += 1
        else:
            result += s[i] + str(count)
            count = 1

    # ✅ handle last group
    result += s[-1] + str(count)

    print("compressed =", result)


# ============================================frequency_count============================================================
def frequency_count():

    import time

    print("===== Frequency Count =====")
    nums = [1, 2, 2, 3, 3, 3]
    freq = {}
    print("counting frequency of", nums)
    time.sleep(2)

    for n in nums:
        if n in freq:
            freq[n] += 1
        else:
            freq[n] = 1

    print(freq)


# ================================================find_max_profit==============================================================
import random


def find_max_profit():

    print("===== Find Max Profit =====")

    prices = [random.randint(1, 20) for _ in range(6)]
    print("Stock prices =", prices)

    min_price = prices[0]
    best_buy = prices[0]
    best_sell = prices[0]
    max_profit = 0

    for p in prices[1:]:

        # check profit if sold today
        if p - min_price > max_profit:
            max_profit = p - min_price
            best_buy = min_price
            best_sell = p

        # update minimum price seen so far
        if p < min_price:
            min_price = p

    print(f"Buy at {best_buy}, Sell at {best_sell}, Profit = {max_profit}")


# ============================================nested_list_reference=======================================================
def nested_list_reference():
    def print_grid_table(title, g):
        print("\n" + "=" * 95)
        print(title)
        print("=" * 95)

        # Header
        print(f"{'Row':<8}{'Row Address':<18}{'Col0':<22}{'Col1':<22}{'Col2':<22}")
        print("-" * 95)

        for r in range(len(g)):
            row_addr = id(g[r])

            c0 = f"{g[r][0]} / {id(g[r][0])}"
            c1 = f"{g[r][1]} / {id(g[r][1])}"
            c2 = f"{g[r][2]} / {id(g[r][2])}"

            print(f"{r:<8}{row_addr:<18}{c0:<22}{c1:<22}{c2:<22}")

    # Wrong Grid (shared rows)
    ngrid = [[0] * 3] * 3

    # Correct Grid (independent rows)
    grid = [[0] * 3 for _ in range(3)]

    print_grid_table("Wrong Grid (Shared Rows)", ngrid)
    print_grid_table("Correct Grid (Independent Rows)", grid)

    # Modify one value to visualize difference
    ngrid[0][0] = 1
    grid[0][0] = 1

    print("\nAFTER CHANGING [0][0] = 1")

    print_grid_table("Wrong Grid After Change", ngrid)
    print_grid_table("Correct Grid After Change", grid)


# ====================================================array_memory_mapping====================================================


def array_memory_mapping():
    import numpy as np

    # ==================================================
    # 1D ARRAY
    # ==================================================
    arr = np.array([10, 20, 30, 40, 50], dtype=np.int64)

    print("=" * 90)
    print("NumPy 1D Array")
    print("=" * 90)

    print(arr)
    print()

    base_addr = arr.ctypes.data

    print("Base Address :", base_addr)
    print("Shape        :", arr.shape)
    print("Data Type    :", arr.dtype)
    print("Item Size    :", arr.itemsize, "bytes")
    print("Strides      :", arr.strides)
    print()

    print("=" * 90)
    print(f"{'Index':<10}{'Value':<10}{'Cell Address':<20}{'Offset(Bytes)':<15}")
    print("=" * 90)

    for i in range(len(arr)):
        cell_addr = base_addr + i * arr.strides[0]
        offset = cell_addr - base_addr

        print(f"{i:<10}{arr[i]:<10}{cell_addr:<20}{offset:<15}")

    print("=" * 90)

    # ==================================================
    # 2D ARRAY
    # ==================================================
    grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int64)

    print("\n" + "=" * 90)
    print("NumPy 2D Grid")
    print("=" * 90)

    print(grid)
    print()

    base_addr = grid.ctypes.data

    print("Base Address :", base_addr)
    print("Shape        :", grid.shape)
    print("Data Type    :", grid.dtype)
    print("Item Size    :", grid.itemsize, "bytes")
    print("Strides      :", grid.strides)
    print()

    print("=" * 90)
    print(f"{'Row':<8}{'Col':<8}{'Value':<10}{'Cell Address':<20}{'Offset(Bytes)':<15}")
    print("=" * 90)

    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):

            cell_addr = base_addr + r * grid.strides[0] + c * grid.strides[1]
            offset = cell_addr - base_addr

            print(f"{r:<8}{c:<8}{grid[r][c]:<10}{cell_addr:<20}{offset:<15}")

    print("=" * 90)


# ====================================================merge_intervals======================================================

import random


def merge_intervals():

    # Static intervals (uncomment to test specific cases)
    # intervals = [[8, 16], [5, 19]]

    # Dynamic random intervals
    # Generate random number of intervals (2 to 5)
    count = random.randint(2, 5)

    intervals = []

    # Create random intervals
    for _ in range(count):
        start = random.randint(1, 15)
        end = random.randint(start, 20)  # end always >= start
        intervals.append([start, end])

    # Alternative one-liner for random intervals
    # intervals = [[random.randint(1, 10), random.randint(11, 20)] for _ in range(6)]

    print("Generated random intervals :", intervals)
    intervals.sort()
    print("intervals after sorting    :", intervals)
    print("Merging intervals.......")

    result = [intervals[0]]

    for start, end in intervals[1:]:
        last = result[-1]

        if start <= last[1]:
            last[1] = end
        else:
            result.append([start, end])

    print("Merged intervals:", result)


# =====================================================sliding_window_sum==================================================


def sliding_window_sum():

    import random

    count = random.randint(5, 15)
    print(f"Generating random array of {count} elements...")
    arr = []

    for _ in range(count):
        arr.append(random.randint(1, 10))
    print(f"arr = {arr}")
    k = 3

    print(f"{'Window':<10}{'Values':<20}{'Sum':<10}")
    print("-" * 40)

    for i in range(len(arr) - k + 1):
        window = arr[i : i + k]
        print(f"{i+1:<10}{str(window):<20}{sum(window):<10}")


# ==============================================remove even numbers===========================================================================

def remove_even_numbers():

    print("===== Remove Even Numbers from List =====")
    
    nums = [1,2,3,4,5,6,7,8]
    print("Original list:", nums)

    for n in nums[:]:          # loop over copy
        if n % 2 == 0:
            nums.remove(n)

    print("List after removing even numbers:", nums)


if __name__ == "__main__":
    # login_system()
    # encryption_lab()
    # string_compression()
    # frequency_count()
    # find_max_profit()
    # nested_list_reference()
    # array_memory_mapping()
    # merge_intervals()
    # sliding_window_sum()
      remove_even_numbers()
    
