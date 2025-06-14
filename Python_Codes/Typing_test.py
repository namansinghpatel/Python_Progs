from faker import Faker
import time

print("welcome to the typing test!")
time.sleep(1)
print("Type the phrase given below to see your results")
time.sleep(1)
words = Faker()
random_phrase = ' '.join(words.word() for _ in range(30))
print("Random Phrase:", random_phrase)
time.sleep(1)
start_time = time.time()
var = input("Please type here: ")
end_time = time.time()

if var == random_phrase:
    print(f"Great you have a 100% accuracy! and you typed in {int(end_time - start_time)} seconds!")
else:
    print("Sorry, you typed with some error please try again")
time.sleep(10)
