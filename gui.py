import vending_machine as vm
import tkinter as tk
from tkinter import messagebox

ROOT_HEIGHT, ROOT_WIDTH = 600, 800
ROOT_BG_COLOR = '#c7dcff'
FRAME_BG_COLOR = '#4d658c'
LABEL_BG_COLOR = '#9ab2d9'
BORDER_SIZE = 5
FRAME_PRODUCTS_X, FRAME_PRODUCTS_Y, FRAME_PRODUCTS_WIDTH, FRAME_PRODUCTS_HEIGHT = 0.5, 0.05, 0.9, 0.28
FRAME_COINS_X, FRAME_COINS_Y, FRAME_COINS_WIDTH, FRAME_COINS_HEIGHT = 0.5, 0.35, 0.9, 0.1
FRAME_VALUE_X, FRAME_VALUE_Y, FRAME_VALUE_WIDTH, FRAME_VALUE_HEIGHT = 0.5, 0.47, 0.9, 0.4
LABEL_SUMMARY_Y, LABEL_SUMMARY_WIDTH, LABEL_SUMMARY_HEIGHT = 0, 0.48, 1
LABEL_PRODUCTS_WIDTH, LABEL_PRODUCTS_HEIGHT = 1, 1
INSERTED_MONEY_LABEL_X, INSERTED_MONEY_LABEL_Y, INSERTED_MONEY_LABEL_WIDTH, INSERTED_MONEY_LABEL_HEIGHT = 0.01, 0.25, 0.17, 0.5
COIN_BUTTON_INIT_X, COIN_BUTTON_Y, COIN_BUTTON_WIDTH, COIN_BUTTON_HEIGHT, COIN_BUTTON_SPACE = 0.19, 0.25, 0.08, 0.5, 0.01
NUM_BUTTON_INIT_X, NUM_BUTTON_INIT_Y, NUM_BUTTON_WIDTH, NUM_BUTTON_HEIGHT, NUM_BUTTONS_AMOUNT = 0.61, 0.18, 0.09, 0.20, 10
LABEL_PRODUCT_ID_X, LABEL_PRODUCT_ID_Y, LABEL_PRODUCT_ID_WIDTH, LABEL_PRODUCT_ID_HEIGHT = 0.61, 0.01, 0.27, 0.15
DEFAULT_LABEL_PRODUCT_ID_TEXT = "Wprowadź numer produktu"
BUY_BUTTON_X, BUY_BUTTON_Y, BUY_BUTTON_WIDTH, BUY_BUTTON_HEIGHT = 0.70, 0.78, 0.09, 0.20
CANCEL_BUTTON_X, CANCEL_BUTTON_Y, CANCEL_BUTTON_WIDTH, CANCEL_BUTTON_HEIGHT = 0.79, 0.78, 0.09, 0.20
PRODUCT_COLUMN_OFFSET = 30
PRODUCTS_IN_A_ROW = 3
NUMS_IN_THE_ROW = 3
PLN_1 = 100
MAX_PRODUCT_ID_LEN = 2


class VendingMachineMainView:
    def __init__(self, root, vending_machine_service, products):
        self.root = root
        self.products = products
        self.vending_machine_service = vending_machine_service
        self.chosen_product_id = ""

        self.frame_coins = self.create_frame_coins(root)
        self.frame_inserted_value = self.create_frame_inserted_value(root)
        self.frame_product_list = self.create_frame_product_list(root)
        self.label_inserted_money = self.create_label_inserted_money()

        self.init_frame_coins_content()
        self.init_frame_product_list_content()
        self.init_frame_inserted_value_content()

    @staticmethod
    def create_frame_coins(root):
        frame_coins = tk.Frame(root, bg=FRAME_BG_COLOR, bd=BORDER_SIZE)
        frame_coins.place(relx=FRAME_COINS_X, rely=FRAME_COINS_Y,
                          relwidth=FRAME_COINS_WIDTH, relheight=FRAME_COINS_HEIGHT, anchor='n')
        return frame_coins

    @staticmethod
    def create_frame_inserted_value(root):
        frame_inserted_value = tk.Frame(root, bg=FRAME_BG_COLOR, bd=BORDER_SIZE)
        frame_inserted_value.place(relx=FRAME_VALUE_X, rely=FRAME_VALUE_Y,
                                   relwidth=FRAME_VALUE_WIDTH, relheight=FRAME_VALUE_HEIGHT, anchor='n')
        return frame_inserted_value

    @staticmethod
    def create_frame_product_list(root):
        frame_product_list = tk.Frame(root, bg=FRAME_BG_COLOR, bd=BORDER_SIZE)
        frame_product_list.place(relx=FRAME_PRODUCTS_X, rely=FRAME_PRODUCTS_Y,
                                 relwidth=FRAME_PRODUCTS_WIDTH, relheight=FRAME_PRODUCTS_HEIGHT, anchor='n')
        return frame_product_list

    def create_label_inserted_money(self):
        label_inserted_money = tk.Label(self.frame_coins, text='Wpłaciłeś: 0zł', anchor="w")
        label_inserted_money.place(relx=INSERTED_MONEY_LABEL_X, rely=INSERTED_MONEY_LABEL_Y,
                                   relwidth=INSERTED_MONEY_LABEL_WIDTH, relheight=INSERTED_MONEY_LABEL_HEIGHT)
        return label_inserted_money

    def init_frame_coins_content(self):
        self.init_coin_buttons()

    def init_coin_buttons(self):
        buttons = []
        for denomination in vm.DENOMINATIONS:
            if denomination < PLN_1:
                text = f"{denomination}gr"
            else:
                text = f"{int(denomination / PLN_1)}zl"

            button = tk.Button(self.frame_coins, text=text, bg='grey',
                               command=lambda d=denomination:
                               self.vending_machine_service.insert_coin(d, self.label_inserted_money))
            buttons.append(button)
        self.place_coin_buttons(buttons)

    @staticmethod
    def place_coin_buttons(buttons):
        relx = COIN_BUTTON_INIT_X
        for button in buttons:
            button.place(relx=relx, rely=COIN_BUTTON_Y, relwidth=COIN_BUTTON_WIDTH, relheight=COIN_BUTTON_HEIGHT)
            relx += COIN_BUTTON_WIDTH + COIN_BUTTON_SPACE

    def init_frame_product_list_content(self):
        label_products = tk.Label(self.frame_product_list, bg=LABEL_BG_COLOR)
        label_products.place(relwidth=LABEL_PRODUCTS_WIDTH, relheight=LABEL_PRODUCTS_HEIGHT)
        self.display_products(label_products)

    def init_frame_inserted_value_content(self):
        label_summary = self.create_label_summary()
        label_product_id = self.create_label_product_id()
        self.init_buy_button(label_summary, label_product_id)
        self.init_product_num_buttons(label_product_id)
        self.init_cancel_button(label_summary, label_product_id)

    def create_label_product_id(self):
        label_product_id = tk.Label(self.frame_inserted_value, anchor="c", text=DEFAULT_LABEL_PRODUCT_ID_TEXT)
        label_product_id.place(relx=LABEL_PRODUCT_ID_X, rely=LABEL_PRODUCT_ID_Y,
                               relwidth=LABEL_PRODUCT_ID_WIDTH, relheight=LABEL_PRODUCT_ID_HEIGHT)
        return label_product_id

    def create_label_summary(self):
        label_summary = tk.Label(self.frame_inserted_value)
        label_summary.place(relwidth=LABEL_SUMMARY_WIDTH, relheight=LABEL_SUMMARY_HEIGHT, rely=LABEL_SUMMARY_Y)
        return label_summary

    def init_buy_button(self, label_summary, label_product_id):
        button_buy = tk.Button(self.frame_inserted_value, text="KUP", bg='grey',
                               command=lambda: self.buy_product_lambda(label_summary, label_product_id))
        button_buy.place(relx=BUY_BUTTON_X, rely=BUY_BUTTON_Y, relwidth=BUY_BUTTON_WIDTH,
                         relheight=BUY_BUTTON_HEIGHT)

    def init_cancel_button(self, label_summary, label_product_id):
        button_cancel = tk.Button(self.frame_inserted_value, text="ANULUJ", bg='grey',
                                  command=lambda:
                                  self.cancel_button_lambda(label_summary, label_product_id))
        button_cancel.place(relx=CANCEL_BUTTON_X, rely=CANCEL_BUTTON_Y, relwidth=CANCEL_BUTTON_WIDTH,
                            relheight=CANCEL_BUTTON_HEIGHT)

    def cancel_button_lambda(self, label_summary, label_product_id):
        self.vending_machine_service.cancel_transaction(label_summary, self.label_inserted_money)
        self.chosen_product_id = ''
        label_product_id['text'] = DEFAULT_LABEL_PRODUCT_ID_TEXT

    def buy_product_lambda(self, label_summary, label_product_id):
        self.vending_machine_service.buy_product(self.chosen_product_id, label_summary, self.label_inserted_money)
        self.chosen_product_id = ""
        label_product_id['text'] = DEFAULT_LABEL_PRODUCT_ID_TEXT

    def init_product_num_buttons(self, label_product_id):
        buttons = []
        for num in range(NUM_BUTTONS_AMOUNT):
            button = tk.Button(self.frame_inserted_value, text=f"{num}",
                               bg='grey',
                               command=lambda n=num: self.update_chosen_product_id(n, label_product_id))
            if num == 0:
                buttons.insert(NUM_BUTTONS_AMOUNT-1, button)
            else:
                buttons.insert(num-1, button)
        self.place_product_num_buttons(buttons)

    @staticmethod
    def place_product_num_buttons(buttons):
        relx = NUM_BUTTON_INIT_X
        rely = NUM_BUTTON_INIT_Y
        for i, button in enumerate(buttons):
            button.place(relx=relx, rely=rely, relwidth=NUM_BUTTON_WIDTH, relheight=NUM_BUTTON_HEIGHT)
            relx += NUM_BUTTON_WIDTH
            if (i+1) % NUMS_IN_THE_ROW == 0:
                rely += NUM_BUTTON_HEIGHT
                relx = NUM_BUTTON_INIT_X

    def update_chosen_product_id(self, num, label_product_id):
        if len(self.chosen_product_id) == MAX_PRODUCT_ID_LEN:
            self.chosen_product_id = ''
        self.chosen_product_id += str(num)
        label_product_id['text'] = self.chosen_product_id

    def display_products(self, label_products):
        max_str_length = max([len(str(product)) for product in self.products])
        for index, product in enumerate(self.products):
            format_width = max_str_length - len(str(product)) + PRODUCT_COLUMN_OFFSET
            label_products['text'] += '{:{width}}'.format(str(product), width=format_width)
            self.product_list_break_line(index, label_products)

    @staticmethod
    def product_list_break_line(index, label_products):
        if index > 1 and (index + 1) % PRODUCTS_IN_A_ROW == 0:
            label_products['text'] += "\n"


class VendingMachineService:
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def buy_product(self, product_id, label_summary, label_inserted_money):
        if not product_id:
            label_summary['text'] = "Wprowadź numer produktu"
        else:
            result = self.vending_machine.buy_product(product_id)
            displayed_text = self.get_displayed_text(result, product_id)
            if result in (vm.BAD_PRODUCT_ID, vm.NOT_ENOUGH_MONEY, vm.STOCK_SHORTAGE):
                self.show_retry_dialog_window(displayed_text, label_summary, label_inserted_money)
            else:
                self.show_transaction_summary(displayed_text, label_summary, label_inserted_money)

    def insert_coin(self, val, label_inserted_money):
        self.vending_machine.insert_coin(val)
        self.print_inserted_money(label_inserted_money)

    def print_inserted_money(self, label_inserted_money):
        if self.vending_machine.inserted_money < PLN_1:
            gr = self.vending_machine.inserted_money
            label_inserted_money['text'] = f"Wpłaciles: {gr} gr"
        else:
            zl = int(self.vending_machine.inserted_money / PLN_1)
            gr = int(self.vending_machine.inserted_money % PLN_1)
            label_inserted_money['text'] = f"Wpłaciles: {zl} zł {gr} gr"

    def get_displayed_text(self, result, product_id):
        switcher = {
            vm.BAD_PRODUCT_ID: "Podaj numer produktu pomiędzy 30 a 50.",
            vm.NOT_ENOUGH_MONEY: "Za mało pieniędzy.",
            vm.STOCK_SHORTAGE: "Produkt niedostepny.",
            vm.BOUGHT_EXACT_CHANGE: f"Kupiłes: {self.vending_machine.find_product_by_id(int(product_id))}",
            vm.UNABLE_TO_GIVE_CHANGE:
                f"Automat nie może wydać reszty.\n"
                f"W celu zakupu proszę umieścić wyliczoną kwotę\n "
                f"{self.print_returned_coins(self.vending_machine.temp_coins)}",
            vm.BOUGHT_RETURNED_CHANGE:
                f"Wydano resztę.\n {self.print_returned_coins(self.vending_machine.change)}"
        }
        displayed_text = switcher.get(result, "Invalid result")
        return displayed_text

    @staticmethod
    def print_returned_coins(coins):
        printed_coins = "Zwrócone monety: \n"
        for key, value in coins.items():
            if value > 0:
                if key < PLN_1:
                    printed_coins += f"{key}gr: x{value}\n"
                else:
                    printed_coins += f"{key/PLN_1}zł: x{value}\n"
        return printed_coins

    def show_retry_dialog_window(self, displayed_text, label_summary, label_inserted_money):
        answer = messagebox.askyesno("Zakup nie powiódł się", f"{displayed_text}\n\nSpróbować ponownie?")
        if not answer:
            self.cancel_transaction(label_summary, label_inserted_money)

    def cancel_transaction(self, label_summary, label_inserted_money):
        label_summary['text'] = self.print_returned_coins(self.vending_machine.temp_coins)
        self.vending_machine.cancel_transaction()
        self.print_inserted_money(label_inserted_money)

    def show_transaction_summary(self, displayed_text, label_summary, label_inserted_money):
        label_summary['text'] = displayed_text
        self.vending_machine.cancel_transaction()
        self.print_inserted_money(label_inserted_money)


def main():
    root = tk.Tk()
    root.configure(background=ROOT_BG_COLOR, height=ROOT_HEIGHT, width=ROOT_WIDTH)
    products = []
    for i in range(7):
        product_id = vm.MIN_PRODUCT_ID+(3*i)
        products.append(vm.Product(product_id, "Coke", 220))
        products.append(vm.Product(product_id+1, "Fanta", 210))
        products.append(vm.Product(product_id+2, "Sprite", 250))

    vending_machine = vm.VendingMachine(products)
    vending_machine_service = VendingMachineService(vending_machine)
    VendingMachineMainView(root, vending_machine_service, products)
    root.mainloop()


if __name__ == '__main__':
    main()
