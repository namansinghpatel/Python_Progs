from colorama import Fore, Back, Style, init
import random
import time

# Initialize colorama
init()


def Guess_The_Number():
    print(Fore.MAGENTA + "Welcome to 'Guess the Number'!")
    print(Fore.GREEN + "I've picked a number between 1 and 100. Can you guess it?")
    print(Fore.RED + "Type 111 to exit !!!")
    print(Style.RESET_ALL)

    attempts = 0

    number_to_guess = random.randint(1, 100)
    # print(f"number_to_guess = {number_to_guess}")

    while True:
        try:
            user_guess = int(input(Fore.CYAN + "Enter your guess: "))
            # print(f"user_guess = {user_guess}")

            attempts += 1

            if user_guess == 111:
                print(
                    Fore.MAGENTA
                    + "Thankyou for playing, please play once again, have fun :) :-)"
                )
                break

            if user_guess < number_to_guess:
                print(Fore.GREEN + "Too low! Try again.")
            elif user_guess > number_to_guess:
                print(Fore.RED + "Too high! Try again.")
            else:
                print(
                    Fore.BLUE
                    + Back.WHITE
                    + f"Congratulations! You guessed the number {number_to_guess} in {attempts} attempts.",
                    end="",
                )
                print(Style.RESET_ALL)
                break
        except:
            print(
                Fore.RED + Back.YELLOW + "This is not a valid integer, try again !",
                end="",
            )
            print(Style.RESET_ALL)


Guess_The_Number()
time.sleep(123456)
