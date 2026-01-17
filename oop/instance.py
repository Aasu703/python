# TODO : create a basic class 
class Book:
    def __init__(self,title,author,pages,price):
        self.title = title
        # TODO : add properties
        self.author = author
        self.pages = pages
        self.price = price
        self.__secret = "Secret"

    # TODO: create instance methods
    def getprice(self):
        if hasattr(self, "_discount"):
            return self.price - (self.price * self._discount)
        else:

            return self.price

    def setdiscount(self, amount):
        self._discount = amount # _discount is a protected property or known as private property

# TODO : create instance of the class
book1 = Book("SO meow","MU_KC", 9866, 1000)
book2 = Book("meow pheow","I_AM_KC", 321, 321)

# TODO : print the class and property
print(book1)
print(book1.title)
print(book2.getprice())
book2.setdiscount(0.25)
print(book2.getprice())

print(book2.__secret)  # This will raise an AttributeError because __secret is a private property