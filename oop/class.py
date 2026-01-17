class Book:

    BOOK_TYPEs = ("HARDCOVER", "PAPERBACK", "EBOOK")

    __booklist =  None


    @classmethod
    def get_book_types(cls):
        return cls.BOOK_TYPEs
    
    def getbooklist():
        if Book.__booklist == None:
            Book.__booklist = []
        return Book.__booklist

    def set_title(self,newtitle):
        self.set_title = newtitle
    
    def __init__(self, title, booktype):
        self.title = title
        if(not booktype in Book.BOOK_TYPEs):
            raise ValueError(f"{booktype} is not a valid book type")
        else:
            self.booktype = booktype


print("Book Types:", Book.get_book_types())

b1 = Book("Title1:", "HARDCOVER")
b2 = Book("Title2:", "PAPERBACK")


thebooks = Book.getbooklist()
thebooks.append(b1)
thebooks.append(b2)

print(thebooks)


