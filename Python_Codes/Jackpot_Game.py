import time
from colorama import init, Fore, Back, Style    
import random
init()

def Guess_the_jackpot():
    number_to_guess = random.randint (1,10)
    attempt = 0
    print(Fore.BLUE + "guess the number between 1 and 10 in 5 or less times to win")
    while True:
        if attempt > 4: 
            print(Fore.RED + "you lose")
            break
        num = int(input(Fore.YELLOW +"please enter your guess: "))
        if number_to_guess == num:
            attempt = attempt + 1
            print(Fore.GREEN + " CONGARTULATIONS!! you have guessed the number in",attempt )
            break
        else:
            attempt = attempt + 1
            if attempt > 5:
                break
            else:
                print(Fore.WHITE + "please try again")   
Guess_the_jackpot()
time.sleep(5)                