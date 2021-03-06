"""This module is responsible for vending machine backend"""

import copy


DENOMINATIONS = [1, 2, 5, 10, 20, 50, 100, 200, 500]
DEFAULT_COIN_QUANTITY = 5
DEFAULT_PRODUCT_QUANTITY = 5
BAD_PRODUCT_ID, NOT_ENOUGH_MONEY, BOUGHT_RETURNED_CHANGE,  STOCK_SHORTAGE, BOUGHT_EXACT_CHANGE, UNABLE_TO_GIVE_CHANGE = range(6)
MIN_PRODUCT_ID, MAX_PRODUCT_ID = 30, 50
PLN_1 = 100


class Product:
    def __init__(self, product_id, name, price):
        """
        Product model class.

        :param product_id: int between 30 and 50
        :param name: str product name
        :param price: int product price in gr
        """
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.product_id}.{self.name}: {int(self.price/PLN_1)}zł {self.price%PLN_1}gr"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self.product_id == other.product_id) and (self.price == other.price) and (self.name == other.name)

    def __hash__(self):
        return hash((self.product_id, self.price, self.name))


class VendingMachine:
    def __init__(self, products):
        """
        This class is responsible for vending machine logic.

        :param products: list of products
        """
        self.coins = {denomination: DEFAULT_COIN_QUANTITY for denomination in DENOMINATIONS}
        self.products = {product: DEFAULT_PRODUCT_QUANTITY for product in products}
        self.temp_coins = self.get_empty_coins_dict()
        self.change = self.get_empty_coins_dict()
        self.inserted_money = 0

    @staticmethod
    def get_empty_coins_dict():
        return {denomination: 0 for denomination in DENOMINATIONS}

    def add_product(self, product, quantity):
        self.products[product] += quantity

    def add_coin(self, coin_value, quantity):
        self.coins[coin_value] += quantity

    def buy_product(self, product_id):
        """
        Method is responsible for buying mechanism.

        :param product_id: int chosen_product_id
        :return: one of 6 defined constants depending on transaction result
        """
        product_id = int(product_id)
        if product_id > MAX_PRODUCT_ID or product_id < MIN_PRODUCT_ID:
            return BAD_PRODUCT_ID
        product = self.find_product_by_id(product_id)
        product_quantity = self.products[product]
        if product_quantity == 0:
            return STOCK_SHORTAGE
        if self.inserted_money >= product.price:
            self.products[product] -= 1
            self.inserted_money -= product.price
            change_status = self.get_change()
            return change_status
        return NOT_ENOUGH_MONEY

    def find_product_by_id(self, product_id):
        """Returns product with given id"""
        for product in self.products:
            if product_id == product.product_id:
                return product

    def get_change(self):
        """
            Method is responsible for giving change.

            Method is called in buying process when inserted_money - product_price >=0.
            It provides giving change algorithm that goal is to use as least coins as possible.

            :return: one of 3 defined constants depending on transaction result
        """
        if self.inserted_money == 0:
            return BOUGHT_EXACT_CHANGE

        all_coins = self.get_all_coins()
        for denomination in sorted(DENOMINATIONS, reverse=True):
            while denomination <= self.inserted_money and self.inserted_money > 0 and all_coins[denomination] > 0:
                all_coins[denomination] -= 1
                self.change[denomination] += 1
                self.inserted_money -= denomination

        if self.inserted_money > 0:
            return UNABLE_TO_GIVE_CHANGE

        self.coins = copy.deepcopy(all_coins)
        return BOUGHT_RETURNED_CHANGE

    def get_all_coins(self):
        """Returns all coins that are in the vending machine"""
        all_coins = copy.deepcopy(self.coins)
        for denomination in DENOMINATIONS:
            all_coins[denomination] += self.temp_coins[denomination]
        return all_coins

    def cancel_transaction(self):
        """Cancels transaction, temporary values are reset"""
        self.inserted_money = 0
        self.temp_coins = self.get_empty_coins_dict()
        self.change = self.get_empty_coins_dict()

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
        self.inserted_money += coin_value


