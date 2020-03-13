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


class VendingMachine:
    def __init__(self):
        self.coins = {Coin(10): 5,
                      Coin(20): 5,
                      Coin(50): 5,
                      Coin(100): 5,
                      Coin(200): 5,
                      Coin(500): 5
                      }
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        print("added product: " + str(product))

    def add_coin(self, coin, quantity):
        self.coins[coin] += quantity
        print(self.coins[coin])

    # def buy_product(self, product_id):


coin1 = Coin(10)
coin2 = Coin(50)
product1 = Product(30, 'Coca-cola', 4)
vending_machine = VendingMachine()
vending_machine.add_coin(coin1, 5)
# vending_machine.add_coin(coin2)
vending_machine.add_product(product1)







