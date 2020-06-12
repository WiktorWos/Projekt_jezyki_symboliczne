import vending_machine as vm
import tkinter as tk
from tkinter import messagebox

CANVAS_HEIGHT, CANVAS_WIDTH = 600, 800
ROOT_BG_COLOR = '#c7dcff'
FRAME_BG_COLOR = '#4d658c'
LABEL_BG_COLOR = '#9ab2d9'
BORDER_SIZE = 5
FRAME_PRODUCTS_X, FRAME_PRODUCTS_Y, FRAME_PRODUCTS_WIDTH, FRAME_PRODUCTS_HEIGHT = 0.5, 0.05, 0.9, 0.28
FRAME_COINS_X, FRAME_COINS_Y, FRAME_COINS_WIDTH, FRAME_COINS_HEIGHT = 0.5, 0.35, 0.9, 0.1
FRAME_VALUE_X, FRAME_VALUE_Y, FRAME_VALUE_WIDTH, FRAME_VALUE_HEIGHT = 0.5, 0.47, 0.9, 0.4
LABEL_SUMMARY_Y, LABEL_SUMMARY_WIDTH, LABEL_SUMMARY_HEIGHT = 0.12, 0.48, 0.88
LABEL_PRODUCTS_WIDTH, LABEL_PRODUCTS_HEIGHT = 1, 1
INSERTED_MONEY_LABEL_X, INSERTED_MONEY_LABEL_Y, INSERTED_MONEY_LABEL_WIDTH, INSERTED_MONEY_LABEL_HEIGHT = 0.01, 0.25, 0.17, 0.5
TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT = 0.52, 0.4, 0.3, 0.15
COIN_BUTTON_INIT_X, COIN_BUTTON_Y, COIN_BUTTON_WIDTH, COIN_BUTTON_HEIGHT = 0.19, 0.25, 0.08, 0.5
BUY_BUTTON_X, BUY_BUTTON_Y, BUY_BUTTON_WIDTH, BUY_BUTTON_HEIGHT = 0.83, 0.4, 0.1, 0.15
PRODUCT_COLUMN_OFFSET = 30


class VendingMachineMainView:
    def __init__(self, root, vending_machine, products):
        self.root = root
        self.products = products
        self.vending_machine = vending_machine

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
        self.init_coin_buttons(self.frame_coins)

    def init_coin_buttons(self, frame_coins):
        buttons = []
        for denomination in vm.DENOMINATIONS:
            if denomination < 100:
                buttons.append(tk.Button(frame_coins, text=f"{denomination}gr",
                                         bg='grey',
                                         command=lambda d=denomination: self.insert_coin(d)))
            else:
                buttons.append(tk.Button(frame_coins, text=f"{int(denomination / 100)}zl",
                                         bg='grey',
                                         command=lambda d=denomination: self.insert_coin(d)))
        self.place_coin_buttons(buttons)

    def init_frame_product_list_content(self):
        label_products = tk.Label(self.frame_product_list, bg=LABEL_BG_COLOR)
        label_products.place(relwidth=LABEL_PRODUCTS_WIDTH, relheight=LABEL_PRODUCTS_HEIGHT)
        self.display_products(label_products)

    def init_frame_inserted_value_content(self):
        label_summary = self.create_label_summary()
        textbox = self.init_textbox()
        self.init_buy_button(textbox, label_summary)

    def create_label_summary(self):
        label_summary = tk.Label(self.frame_inserted_value)
        label_summary.place(relwidth=LABEL_SUMMARY_WIDTH, relheight=LABEL_SUMMARY_HEIGHT, rely=LABEL_SUMMARY_Y)
        return label_summary

    def init_textbox(self):
        textbox = tk.Entry(self.frame_inserted_value, font=40)
        textbox.place(relx=TEXTBOX_X, rely=TEXTBOX_Y, relwidth=TEXTBOX_WIDTH, relheight=TEXTBOX_HEIGHT)
        return textbox

    def init_buy_button(self, textbox, label_summary):
        button_buy = tk.Button(self.frame_inserted_value, text="Wybierz", bg='grey',
                               command=lambda: self.buy_product(textbox.get(), label_summary))
        button_buy.place(relx=BUY_BUTTON_X, rely=BUY_BUTTON_Y, relwidth=BUY_BUTTON_WIDTH,
                         relheight=BUY_BUTTON_HEIGHT)

    def buy_product(self, product_id, label_summary):
        if product_id == '':
            label_summary['text'] = "Wprowadź numer produktu"
        else:
            result = self.vending_machine.buy_product(product_id)
            displayed_text = self.get_displayed_text(result, product_id)
            if result in (vm.BAD_PRODUCT_ID, vm.NOT_ENOUGH_MONEY, vm.STOCK_SHORTAGE):
                self.show_retry_dialog_window(displayed_text, label_summary)
            else:
                self.show_transaction_summary(displayed_text, label_summary)

    def insert_coin(self, val):
        self.vending_machine.insert_coin(val)
        self.print_inserted_money()

    def print_inserted_money(self):
        if self.vending_machine.inserted_money < 100:
            self.label_inserted_money['text'] = f"Wpłaciles: {self.vending_machine.inserted_money} gr"
        else:
            zl = int(self.vending_machine.inserted_money / 100)
            gr = int(self.vending_machine.inserted_money % 100)
            self.label_inserted_money['text'] = f"Wpłaciles: {zl} zł {gr} gr"

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
                if key < 100:
                    printed_coins += f"{key}gr: x{value}\n"
                else:
                    printed_coins += f"{key/100}zł: x{value}\n"
        return printed_coins

    def show_retry_dialog_window(self, displayed_text, label_summary):
        answer = messagebox.askyesno("Zakup nie powiódł się", f"{displayed_text}\n\nSpróbować ponownie?")
        if not answer:
            label_summary['text'] = self.print_returned_coins(self.vending_machine.temp_coins)
            self.vending_machine.clear_temporary_coin_values()
            self.print_inserted_money()

    def show_transaction_summary(self, displayed_text, label_summary):
        label_summary['text'] = displayed_text
        self.vending_machine.clear_temporary_coin_values()
        self.print_inserted_money()

    @staticmethod
    def place_coin_buttons(buttons):
        relx = COIN_BUTTON_INIT_X
        for button in buttons:
            button.place(relx=relx, rely=COIN_BUTTON_Y, relwidth=COIN_BUTTON_WIDTH, relheight=COIN_BUTTON_HEIGHT)
            relx += 0.09

    def display_products(self, label_products):
        max_str_length = max([len(str(product)) for product in self.products])
        for index, product in enumerate(self.products):
            format_width = max_str_length - len(str(product)) + PRODUCT_COLUMN_OFFSET
            label_products['text'] += '{:{width}}'.format(str(product), width=format_width)
            self.product_list_break_line(index, label_products)
    @staticmethod
    def product_list_break_line(index, label_products):
        if index > 1 and (index + 1) % 3 == 0:
            label_products['text'] += "\n"


def main():
    root = tk.Tk()
    root.configure(background=ROOT_BG_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    products = [
            vm.Product(30, "Coca Cola", 220),
            vm.Product(31, "Fanta", 210),
            vm.Product(32, "Coca Cola", 220),
            vm.Product(33, "Fanta", 210),
            vm.Product(34, "Coca Cola", 220),
            vm.Product(35, "Fanta", 210),
            vm.Product(36, "Coca Cola", 220),
            vm.Product(37, "Fanta", 210),
            vm.Product(38, "Coca Cola", 220),
            vm.Product(39, "Fanta", 210),
            vm.Product(40, "Coca Cola", 220),
            vm.Product(41, "Fanta", 210),
            vm.Product(42, "Coca Cola", 220),
            vm.Product(43, "Fanta", 210),
            vm.Product(44, "Coca Cola", 220),
            vm.Product(45, "Fanta", 210),
            vm.Product(46, "Coca Cola", 220),
            vm.Product(47, "Fanta", 210),
            vm.Product(48, "Coca Cola", 220),
            vm.Product(49, "Fanta", 210),
            vm.Product(50, "Coca Cola", 220)
        ]
    vending_machine = vm.VendingMachine(products)
    VendingMachineMainView(root, vending_machine, products)
    root.mainloop()


if __name__ == '__main__':
    main()
