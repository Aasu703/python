class Book:
    def __init__(self, title):
        self.title = title

class Newspaper:
    def __init__(self, name):
        self.name = name

# instances of the object
b1 = Book("One Piece")
b2 = Book("Naruto")
n1 = Newspaper("ktm_post")
n2 = Newspaper("bagmanti_kabhar")

print(type(b1))
print(type(n1))

# comparing two types 
print(type(b1) == type(b2)) # true
print(type(b1) == type(n1)) # false

print(isinstance(b1, Book)) # to check the instance to a known type  
print(isinstance(n1, Book))

