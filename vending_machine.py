import copy


DENOMINATIONS = [1, 2, 5, 10, 20, 50, 100, 200, 500]
DEFAULT_COIN_QUANTITY = 5
DEFAULT_PRODUCT_QUANTITY = 5
BAD_PRODUCT_ID, NOT_ENOUGH_MONEY, BOUGHT, STOCK_SHORTAGE = range(4)
MIN_PRODUCT_ID, MAX_PRODUCT_ID = 30, 50


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"id: {self.product_id}, name: {self.name}, price: {self.price}"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self.product_id == other.product_id) and (self.price == other.price) and (self.name == other.name)

    def __hash__(self):
        return hash((self.product_id, self.price, self.name))


class VendingMachine:
    def __init__(self, products):
        self.coins = {denomination: DEFAULT_COIN_QUANTITY for denomination in DENOMINATIONS}
        self.products = {product: DEFAULT_PRODUCT_QUANTITY for product in products}
        self.temp_coins = self.get_initial_temp_coins()
        self.inserted_money = 0

    def get_initial_temp_coins(self):
        coins = copy.deepcopy(self.coins)
        for coin in coins:
            coins[coin] = 0
        return coins

    def add_product(self, product, quantity):
        self.products[product] += quantity
        print(f"added product: {product}")

    def add_coin(self, coin_value, quantity):
        self.coins[coin_value] += quantity
        print(self.coins[coin_value])

    def buy_product(self, product_id):
        product_id = int(product_id)
        product = self.find_product_by_id(product_id)
        product_quantity = self.products[product]
        if product_quantity == 0:
            return STOCK_SHORTAGE
        if self.inserted_money >= product.price:
            self.products[product] -= 1
            self.print_products()
            self.inserted_money -= product.price
            if self.inserted_money > 0:
                print(f"reszta: {self.inserted_money}")
                self.inserted_money = 0
            return BOUGHT
        return NOT_ENOUGH_MONEY

    def find_product_by_id(self, product_id):
        for product in self.products:
            if product_id == product.product_id:
                return product

    def print_coins(self):
        for coin, quantity in self.coins.items():
            print(f"Coin: {coin}, quantity: {quantity}")

    def print_products(self):
        for product, quantity in self.products.items():
            print(f"Product: {product}, quantity: {quantity}")

    def print_temp_coins(self):
        for coin, quantity in self.temp_coins.items():
            print(f"Coin: {coin}, quantity: {quantity}")

    def insert_coin(self, coin_value):
        self.temp_coins[coin_value] += 1
        self.print_temp_coins()
        self.inserted_money += coin_value






