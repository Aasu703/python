# 1. Hello, You!
# Write a program that asks the user for their name and prints "Hello, [name]!"

# name = input("What is your name? ")
# print(f"Hello, {name}!")

# 2. Even or Odd
# Given a number, print whether it's even or odd.

# number = input("Enter your number: ")
# num = int(number)
# if num % 2 == 0:
#     print(f"{num}, number is even")
# else:
#     print(f"{num},  number is odd")

# simple calculator 
# number1 = int(input("Enter your first number: "))
# number2 = int(input("Enter your second number: "))

# operation = input("Enter the operation you want to perform (+, -, *, /): ")
# if operation == "+":
#     result = number1 + number2
#     print(f"The result of {number1} + {number2} is: {result}")
# elif operation == "-":
#     result = number1 - number2
#     print(f"The result of {number1} - {number2} is: {result}")
# elif operation == "*":
#     result = number1 * number2
#     print(f"The result of {number1} * {number2} is: {result}")
# elif operation == "/":
#     if number2 != 0:
#         result = number1 / number2
#         print(f"The result of {number1} / {number2} is: {result}")
#     else:
#         print("Error: Division by zero is not allowed.")
# else:
#     print("Invalid operation. Please enter one of the following: +, -, *, /.")



# 4. FizzBuzz
# Print numbers 1–50. For multiples of 3 print "Fizz", for multiples of 5 print "Buzz", for both print "FizzBuzz".

# for i in range(1, 51):
#     if i % 3 == 0 and i % 5 == 0:
#         print("FizzBuzz")
#     elif i % 3 == 0:
#         print("Fizz")
#     elif i % 5 == 0:
#         print("Buzz")
#     else:
#         print(i)
    

# reverse a string
reverse_string = input("Enter a string to reverse: ")
reversed_string = reverse_string[::-1] # this is a slicing technique that takes the string and reverses it by starting from the end and moving to the beginning with a step of -1
print(f"Reversed string: {reversed_string}")

