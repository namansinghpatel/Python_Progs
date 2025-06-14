from colorama import Fore, Back, Style, init
init()
print(Fore.MAGENTA + "guess a number between 1 and 10")
a = int (input(Fore.RED + "multiplyit by 2 and write it here- "))
b = int (input(Fore.MAGENTA + "add 5 to it and write it here- "))
c = int (input(Fore.YELLOW + "subtract 7 from it and write it here- "))
d = int (input("add 3 to it and write it here- "))
e = int (input(Fore.RED + "subtract 1 from it and write it here- "))
f = int (input(Fore.CYAN + "multiply it by 3  and write it here- "))
g = f/6
print(Fore.GREEN + "your number is",g)