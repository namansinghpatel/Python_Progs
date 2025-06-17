count = 0
num = int(input("Please enter your number: "))
if num < 0:
    print("you cannot enter a negetive number")
    exit(0)
if num % 10 == 2:
    print("your number has first digit as two")
while num > 0:
    if num < 0:
        print("you cannot enter a negetive number")
    if num % 10 == 2:
        count = count + 1
    num = int(num / 10)
print(f"your number has {count} times two")
