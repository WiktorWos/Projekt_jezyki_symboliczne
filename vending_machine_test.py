import unittest
import vending_machine as vm


class VendingMachineTest(unittest.TestCase):
    def setUp(self):
        self.products = self.get_products()
        self.vending_machine = vm.VendingMachine(self.products)

    @staticmethod
    def get_products():
        products = []
        for i in range(7):
            product_id = vm.MIN_PRODUCT_ID + (3 * i)
            products.append(vm.Product(product_id, "Coke", 220))
            products.append(vm.Product(product_id + 1, "Fanta", 210))
            products.append(vm.Product(product_id + 2, "Sprite", 250))
        return products

    def test_default_coins(self):
        coins = self.vending_machine.coins
        coins_size = len(coins)
        expected_size = len(vm.DENOMINATIONS)
        for key in coins:
            self.assertEqual(coins[key], vm.DEFAULT_COIN_QUANTITY)
        self.assertEqual(coins_size, expected_size)

    def test_default_products(self):
        actual_products = self.vending_machine.products
        actual_products_size = len(actual_products)
        expected_size = len(self.products)
        for key in actual_products:
            self.assertEqual(actual_products[key], vm.DEFAULT_PRODUCT_QUANTITY)
        self.assertEqual(actual_products_size, expected_size)

    def test_get_empty_coins(self):
        empty_coins = self.vending_machine.get_empty_coins_dict()
        coins_size = len(empty_coins)
        expected_size = len(vm.DENOMINATIONS)
        for key in empty_coins:
            self.assertEqual(empty_coins[key], 0)
        self.assertEqual(coins_size, expected_size)

    def test_insert_coin(self):
        self.vending_machine.insert_coin(100)
        self.assertEqual(1, self.vending_machine.temp_coins[100])
        self.assertEqual(100, self.vending_machine.inserted_money)

    def test_find_product_by_id(self):
        product = self.products[0]
        product_id = product.product_id
        returned_product = self.vending_machine.find_product_by_id(product_id)
        self.assertEqual(returned_product, product)

    def test_buy_product_with_exact_coins_value_should_return_BOUGHT_EXACT_CHANGE(self):
        product = self.products[0]
        product_id = product.product_id
        self.vending_machine.insert_coin(200)
        self.vending_machine.insert_coin(20)
        returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.BOUGHT_EXACT_CHANGE)

    def test_buy_product_with_more_coins_value_should_return_BOUGHT_RETURNED_CHANGE(self):
        product = self.products[0]
        product_id = product.product_id
        self.vending_machine.insert_coin(200)
        self.vending_machine.insert_coin(20)
        self.vending_machine.insert_coin(100)
        returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.BOUGHT_RETURNED_CHANGE)

    def test_buy_product_with_stock_shortage_should_return_STOCK_SHORTAGE(self):
        product = self.products[0]
        product_id = product.product_id
        returned_value = -1
        for i in range(vm.DEFAULT_PRODUCT_QUANTITY + 1):
            self.vending_machine.inserted_money = product.price
            returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.STOCK_SHORTAGE)

    def test_buy_product_with_wrong_product_id_should_return_BAD_PRODUCT_ID(self):
        product_ids = [100, 10]
        for product_id in product_ids:
            returned_value = self.vending_machine.buy_product(product_id)
            self.assertEqual(returned_value, vm.BAD_PRODUCT_ID)

    def test_insert_coins_cancel_transaction(self):
        coins_before = self.vending_machine.coins
        self.vending_machine.insert_coin(100)
        self.vending_machine.insert_coin(500)
        self.vending_machine.insert_coin(50)
        self.vending_machine.cancel_transaction()
        for key in self.vending_machine.temp_coins:
            self.assertEqual(self.vending_machine.temp_coins[key], 0)
        self.assertDictEqual(coins_before, self.vending_machine.coins)

    def test_buy_product_with_only_1gr_exact_value_should_return_BOUGHT_EXACT_CHANGE(self):
        product = self.products[0]
        product_id = product.product_id
        for i in range(product.price):
            self.vending_machine.insert_coin(1)
        returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.BOUGHT_EXACT_CHANGE)

    def test_buy_product_with_not_enough_money_should_return_NOT_ENOUGH_MONEY(self):
        product = self.products[0]
        product_id = product.product_id
        self.vending_machine.insert_coin(1)
        returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.NOT_ENOUGH_MONEY)

    def test_buy_product_vending_machine_cannot_give_change_should_return_UNABLE_TO_GIVE_CHANGE(self):
        for key in self.vending_machine.coins:
            self.vending_machine.coins[key] = 0
        product = self.products[0]
        product_id = product.product_id
        self.vending_machine.insert_coin(500)
        returned_value = self.vending_machine.buy_product(product_id)
        self.assertEqual(returned_value, vm.UNABLE_TO_GIVE_CHANGE)

    def test_get_change_should_return_BOUGHT_RETURNED_CHANGE(self):
        expected_change = 50
        self.vending_machine.inserted_money = 50
        self.vending_machine.get_change()
        actual_change = 0
        for key, value in self.vending_machine.change.items():
            actual_change += key * value
        self.assertEqual(expected_change, actual_change)
        self.assertEqual(self.vending_machine.coins[50], vm.DEFAULT_COIN_QUANTITY-1)


if __name__ == '__main__':
    unittest.main()
