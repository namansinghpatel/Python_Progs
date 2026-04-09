email = input("Enter email: ")

if any(ch.isupper() for ch in email):
    print(f"Invalid Email: uppercase not allowed")
elif " " in email:
    print("Invalid Email: space not allowed")
elif "@" in email and "." in email:
    print("Valid email address")
else:
    print("Invalid Email: missing @ or .")