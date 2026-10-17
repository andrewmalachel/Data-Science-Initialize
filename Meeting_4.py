friends_list = ['Amanda', 'Bruno', 'Camila', 'Drake', 'Elvis', 'Freddie', 'George', 'Harry', 'Iggy', 'Joji']

for i in friends_list:
    print(i)

print("<-><-><->")

for i in range(3):
    print(friends_list[i])

print("<-><-><->")

for i in range(1, 11, 2):
    print(friends_list[i])

print("<-><-><->")

fruits = ['banana', 'apple', 'mango']
names = ['Alice', 'Bob', 'Charlie']

for fruit in fruits:
    for name in names:
        print(f"{name} likes {fruit}")

print("<-><-><->")

for i in range(1, 6):
    for j in range(1, i+1):
        print("*", end="")
    print()

print("<-><-><->")

for i in range(1, 6):
    for j in range(1, 6):
        print("*", end=" ")
    print()

print("<->Exercise Start<->")

for i in range(3, 101, 3):
    print(i)

print("<->Exercise End<->")

i = 1
while i <= 10:
    print("*" * i)
    i += 1

print("<->Exercise Start<->")

saving = 0 
week = 0 

while saving < 100:
   saving += 10  
   week += 1     

# Menampilkan hasil 
print("Ali needs", week, "weeks to collect $100.")

print("<->Exercise 2 Start<->")
"""
import random

secret_number = random.randint(1, 10)

guess = None

while guess != secret_number:
    guess = int(input("Guess the secret number between 1 and 10: "))

    if guess == secret_number:
        print("Congratulations! You guessed the secret number:", secret_number)

"""

print("<->Exercise Ended<->")

i = 1

while i <= 3:
    print("i'm learning Python") 
    i += 1