email = input("Enter email: ")

if (ch.isupper() for ch in email):
    print("Invalid Email")
elif " " in email :
    print("Email is InValid ")
elif "@" and  "."  in email :
    print("Valid email ")
else :
    print("Email is Invalid")