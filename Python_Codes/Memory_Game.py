from colorama import Fore, Back, Style, init
import random
import time
import os

print(Fore. MAGENTA + "Welcome to the memory game!")
time.sleep(2)
print(Fore. WHITE + "A number will be shown and you have to guess it")
time.sleep(2)
for step in range(10):
    print(Fore.YELLOW + f"LEVEL {step + 1}")
    time.sleep(2)
    start = 10**(step)   
    end = 10**(step + 1) - 1      
    random_number = random.randint(start, end)
    print(Fore.CYAN + f"Memorize this number: {random_number}")
    time.sleep(step/2 + 1)
    os.system('cls')
    time.sleep(1)
    num = int(input(Fore.GREEN + "please enter the number you memorised: "))
    if num == random_number:
        print(Fore.BLUE + "Great memory!!")
        if step == 9:
            print(Fore.WHITE + "Congrats you have completed this game!!") 
    else:
        time.sleep(1)
        print(Fore.RED + f"sorry the number was {random_number} you reached till LEVEL {step} better luck next time")
        break

time.sleep(10)    