ticker = "GOOG"
price = 185.43
company = "Google LLC"

class Stock:
    def __init__(self, ticker, price, company):
        self.ticker = ticker
        self.price = price
        self.company = company

    def get_description(self):
        return f"{self.ticker}: {self.company} -- ${self.price}"



# DO NOT change this code:
symbol = Stock(ticker, price, company)

description = symbol.get_description()

print(symbol.get_description())