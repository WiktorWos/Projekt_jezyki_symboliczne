import copy


class Coin:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "value: " + str(self.value)

    def __eq__(self, other):
        if not isinstance(other, Coin):
            return NotImplemented

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return "id: " + str(self.product_id) + ", name:" + str(self.name) + ", price: " + str(self.price)

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented

        return (self.product_id == other.product_id) and (self.price == other.price) and (self.name == other.name)

    def __hash__(self):
        return hash((self.product_id, self.price, self.name))


class VendingMachine:
    def __init__(self):
        self.coins = {
            Coin(1): 5,
            Coin(2): 5,
            Coin(5): 5,
            Coin(10): 5,
            Coin(20): 5,
            Coin(50): 5,
            Coin(100): 5,
            Coin(200): 5,
            Coin(500): 5
        }
        self.products = {
            Product(30, "Coca-cola", 300): 5,
            Product(31, "Fanta", 280): 5,
        }
        self.temp_coins = self.get_initial_temp_coins()
        self.inserted_money = 0

    def get_initial_temp_coins(self):
        coins = copy.deepcopy(self.coins)
        for coin in coins:
            coins[coin] = 0
        return coins

    def add_product(self, product, quantity):
        self.products[product] += quantity
        print("added product: " + str(product))

    def add_coin(self, coin, quantity):
        self.coins[coin] += quantity
        print(self.coins[coin])

    def buy_product(self, product_id):
        paid = 0
        for product in self.products:
            if product_id == product.product_id:
                while paid < product.price:
                    coin_value = int(input("please insert a coin: \n"))
                    paid += coin_value
                    self.add_coin(Coin(coin_value), 1)
                if paid > product.price:
                    print("reszta: " + str(paid - product.price))
                print("Kupiony produkt: " + str(product))
                self.print_coins()

    def print_coins(self):
        for coin in self.coins:
            print("Coin: " + str(coin) + " quantity: " + str(self.coins[coin]))

    def print_temp_coins(self):
        for coin in self.temp_coins:
            print("Coin: " + str(coin) + " quantity: " + str(self.temp_coins[coin]))

    def insert_coin(self, val):
        coin = Coin(val)
        self.temp_coins[coin] += 1
        self.print_temp_coins()
        self.inserted_money += val


vending_machine = VendingMachine()
vending_machine.insert_coin(1)






