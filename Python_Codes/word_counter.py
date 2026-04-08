def count_words(sentence):
    count = 0
    in_word = False 

    for ch in sentence:
        if ch != " " and not in_word:
            count += 1
            in_word = True
        elif ch == " ":
            in_word = False

    return count


# 🔍 Test cases
test_cases = [
    "hello world",
    "   hello world",
    "hello   world",
    "   hello   world  ",
    "",
    "one",
    "   ",
    "python is fun",
    "  multiple   spaces   here "
]

# Run tests
for t in test_cases:
    print(f"Input: '{t}'")
    print("Word count:", count_words(t))
    print("-" * 30)