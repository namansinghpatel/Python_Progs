from numbers import Number


def fibonacci(buggy=False):
    print("\nFibonacci Sequence:")
    n = 5
    a, b = 0, 1

    # 🐞 Buggy Code
    # for i in range(n):
    #     print(a)
    #     a = b
    #     b = a + b

    for _ in range(n):
        print(a)
        if buggy:
            a = b
            b = a + b   # ❌ wrong logic
        else:
            a, b = b, a + b  # ✅ correct


def list_search(buggy=False):
    nums = [2, 4, 6, 8]
    target = 7
    print(f"Find the target number {target} in the list: {nums} ")

    # 🐞 Buggy Code
    # found = False
    # for n in nums:
    #     if n == target:
    #         found = True
    #     else:
    #         found = False

    found = False
    for n in nums:
        if n == target:
            found = True
            if not buggy:
                break
        else:
            if buggy:
                found = False  # ❌ overwriting

    print("Found:", found)


def remove_duplicates(buggy=False):
    print("Remove duplicates from the string: 'programming'")
    text = "programming"
    result = ""

    # 🐞 Buggy Code
    # for ch in text:
    #     if ch not in result:
    #         result = ch

    for ch in text:
        if ch not in result:
            if buggy:
                result = ch      # ❌ overwrite
            else:
                result += ch     # ✅ append

    print("\nResult:", result)


def count_words(buggy=False):
    print("Count the number of words in a sentence.")
    sentence = "Hello world this is a test"
    print(f"Sentence: {sentence}")

    # 🐞 Buggy Code
    # count = 1
    # for ch in sentence:
    #     if ch == " ":
    #         count += 1

    if buggy:
        count = 1
        for ch in sentence:
            if ch == " ":
                count += 1
    else:
        count = 0
        in_word = False

        for ch in sentence:
            if ch != " " and not in_word:
                count += 1
                in_word = True
            elif ch == " ":
                in_word = False

    print("Words:", count)


def sum_list(buggy=False):
    nums = [1, 2, 3, 4]
    print(f"Find the sum of numbers in the list {nums}")
    total = 0

    # 🐞 Buggy Code
    # for n in nums:
    #     total =+ n

    for n in nums:
        if buggy:
            total =+ n   # ❌ wrong
        else:
            total += n   # ✅ correct

    print("\nSum:", total)


def max_number(buggy=False):
    nums = [5, 9, 2, 11, 3, 7, 1,  4, 8, 6, 27, 15, 20, 12, 18, 25, 37, 22, 23, 26, 28, 29]
    print(f"Find the max number in the list: {nums}")
    max_val = nums[0]

    # 🐞 Buggy Code
    # for i in range(len(nums)):
    #     if nums[i] > max:
    #         max = i

    for i in range(len(nums)):
        if nums[i] > max_val:
            if buggy:
                max_val = i        # ❌ wrong
            else:
                max_val = nums[i]  # ✅ correct

    print("\nMax:", max_val)


def reverse_number(buggy=False):
    num = 12345
    print(f"Reverse the number: {num}")
    rev = 0

    # 🐞 Buggy Code
    # while num > 0:
    #     digit = num % 10
    #     rev = digit
    #     num = num // 10

    while num > 0:
        digit = num % 10
        if buggy:
            rev = digit            # ❌ overwrite
        else:
            rev = rev * 10 + digit # ✅ correct
        num = num // 10

    print("\nReversed:", rev)

def sum_of_even_numbers(buggy=False):
    nums = [1, 2, 3, 4, 5, 6]
    print(f"Find the sum of even numbers in the list: {nums}")
    total = 0

    # 🐞 Buggy Code
    # for n in nums:
    #      if n % 2 == 0:
    #          total = n

    # print(total)

    for n in nums:
       if n % 2 == 0:
              if buggy:
                total = n       # ❌ overwrite
              else:
                total = total + n    # ✅ correct

    print(total)

def count_digits_in_number(buggy=False):
    num = 12345
    print(f"Count the number of digits in the number: {num}")
    count = 0

    # 🐞 Buggy Code
    #  while num > 0:
    #      num = num // 10

    #  print(count)

    while num > 0:
        if buggy:
            num = num // 10        # ❌ missing count increment
        else:
            num = num // 10         # ✅ correct
            count += 1 
    print(count)

def exec_all(buggy=False):
    print("\nRunning all functions in buggy mode:", buggy)
    fibonacci(buggy)
    list_search(buggy)
    remove_duplicates(buggy)
    count_words(buggy)
    sum_list(buggy)
    max_number(buggy)
    reverse_number(buggy)
    sum_of_even_numbers(buggy)
    count_digits_in_number(buggy)

# 🔥 MENU
while True:
    print("\n==== Debug Practice Menu ====")
    print("1. Fibonacci")
    print("2. List Search")
    print("3. Remove Duplicates")
    print("4. Count Words")
    print("5. Sum List")
    print("6. Max Number")
    print("7. Reverse Number")
    print("8. Sum of Even Numbers")
    print("9. Count Digits in Number")
    print("10. Run All")
    print("0. Exit")

    choice = input("Choose option: ")

    if choice == "0":
        break

    mode = input("Run buggy version? (y/n): ").lower()
    buggy = (mode == "y")

    if choice == "1":
        fibonacci(buggy)
    elif choice == "2":
        list_search(buggy)
    elif choice == "3":
        remove_duplicates(buggy)
    elif choice == "4":
        count_words(buggy)
    elif choice == "5":
        sum_list(buggy)
    elif choice == "6":
        max_number(buggy)
    elif choice == "7":
        reverse_number(buggy)
    elif choice == "8":
        sum_of_even_numbers(buggy)
    elif choice == "9":
        count_digits_in_number(buggy)
    elif choice == "10":
        exec_all(buggy)
    else:
        print("Invalid choice")