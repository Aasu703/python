# TODO : create a basic class 
class Book:
    def __init__(self,title,author,pages,price):
        self.title = title
        # TODO : add properties
        self.author = author
        self.pages = pages
        self.price = price

    # TODO: create instance methods
    def getprice(self):
        return self.price

# TODO : create instance of the class
book1 = Book("SO meow","MU_KC", 9866, 1000)
book2 = Book("meow pheow","I_AM_KC", 321, 321)

# TODO : print the class and property
print(book1)
print(book1.title)