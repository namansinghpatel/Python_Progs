import random
import time
from colorama import Fore, Back, Style, init


def process_input(value):
    try:
        # Try converting the input to an integer
        return int(value)
    except ValueError:
        # If conversion fails, return as a string
        return value


var1 = "rock"
var2 = "paper"
var3 = "scissors"
var4 = 0
var5 = 1
var6 = 2
user = 0
comp = 0
print(Fore.MAGENTA + "Welcome to the 'Rock Paper Scisor' game!! ")
time.sleep(1)
print(Fore.CYAN + "Beat the computer in best of 5 and win the game!")
time.sleep(1)
while comp < 5 and user < 5:
    entry = input(
        Fore.YELLOW + "Enter your choice (rock or 0, paper or 1, scissors or 2): "
    )
    entry = process_input(entry)
    if entry in [var1, var2, var3, var4, var5, var6]:
        comp_choice = [var1, var2, var3][random.randint(0, 2)]
        print(Fore.WHITE + f"the choice of computer is {comp_choice} ")
        if (
            (comp_choice == var1 and (entry == var1 or entry == var4))
            or (comp_choice == var2 and (entry == var2 or entry == var5))
            or (comp_choice == var3 and (entry == var3 or entry == var6))
        ):
            time.sleep(1)
            print(Fore.BLUE + "draw")
            time.sleep(1)
            print(Fore.CYAN + f"your score = {user} and comp score = {comp}")
            time.sleep(1)
        elif (
            (comp_choice == var1 and (entry == var2 or entry == var5))
            or (comp_choice == var2 and (entry == var3 or entry == var6))
            or (comp_choice == var3 and (entry == var1 or entry == var4))
        ):
            user = user + 1
            time.sleep(1)
            print(Fore.GREEN + "you win this round")
            time.sleep(1)
            print(Fore.CYAN + f"your score = {user} and comp score = {comp}")
            time.sleep(1)
        elif (
            (comp_choice == var1 and (entry == var3 or entry == var6))
            or (comp_choice == var2 and (entry == var1 or entry == var4))
            or (comp_choice == var3 and (entry == var2 or entry == var5))
        ):
            comp = comp + 1
            time.sleep(1)
            print(Fore.RED + "comp win this round")
            time.sleep(1)
            print(Fore.CYAN + f"your score = {user} and comp score = {comp}")
            time.sleep(1)
        else:
            print("ERROR")

    else:
        print(Fore.RED + "please enter the correct choice @#$%%##@@ ")
if user == 5:
    print(Fore.GREEN + "Congratulations!! You won this game ")
else:
    print(Fore.MAGENTA + "Comp won this game! Better luck next time ")
time.sleep(10)
