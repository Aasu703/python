# # Functions 
# # a piece of reusable code that performs a specific task
# fam=[1.4,2.5,3.6,4.7]
# max(fam)
# print(max(fam))

# # how to define a function 
# def greet(): # defining a function 
#     print("Hello, welcome to the world of functions!")
#     if True:
#         print("This is inside the function.")   # inisde the function block
#     else: 
#         print("This will never be printed.")
# greet() # calling the function



# # Create variables var1 and var2
# var_1 = [1,2,3,4,5]
# var_2 = False #True = 1, False = 0

# # Print out type of var_1 
# print(type(var_1))

# #Print out length of var_1
# print(len(var_1))

# #Convert var_2 to integer and print out the result
# print(int(var_2))   

# # HELP --- IN PYTHONSHELL TYPE HELP() AND PASS THE FUNCTION NAME AS ARGUMENT
# help(len)

# help(int)


# Create lists first and second
first = [11.25, 18.0, 20.0]
second = [10.75, 9.50]

# Paste together first and second: full
full = first + second

# Sort full in descending order: full_sorted
full_sorted = sorted(full, reverse=True)

# Print out full_sorted
print(full_sorted)