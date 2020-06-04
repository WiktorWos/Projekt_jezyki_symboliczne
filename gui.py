import vending_machine as vm
import tkinter as tk
from tkinter import messagebox

CANVAS_HEIGHT, CANVAS_WIDTH = 500, 600
FRAME_BG_COLOR = '#9c978a'
BORDER_SIZE = 5
FRAME_COINS_X, FRAME_COINS_Y, FRAME_COINS_WIDTH, FRAME_COINS_HEIGHT = 0.5, 0.05, 0.9, 0.1
FRAME_VALUE_X, FRAME_VALUE_Y, FRAME_VALUE_WIDTH, FRAME_VALUE_HEIGHT = 0.5, 0.17, 0.9, 0.4
LABEL_WIDTH, LABEL_HEIGHT = 0.48, 1
TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT = 0.52, 0.4, 0.3, 0.15
COIN_BUTTON_INIT_X, COIN_BUTTON_Y, COIN_BUTTON_WIDTH, COIN_BUTTON_HEIGHT = 0.01, 0.25, 0.1, 0.5
BUY_BUTTON_X, BUY_BUTTON_Y, BUY_BUTTON_WIDTH, BUY_BUTTON_HEIGHT = 0.83, 0.4, 0.1, 0.15


def insert_coin(vending_machine, label, val):
    vending_machine.insert_coin(val)
    if vending_machine.inserted_money < 100:
        label['text'] = f"Wplaciles {vending_machine.inserted_money} gr"
    else:
        zl = int(vending_machine.inserted_money / 100)
        gr = int(vending_machine.inserted_money % 100)
        label['text'] = f"Wplaciles: {zl} zl {gr} gr"


def buy_product(vending_machine, label, product_id):
    if product_id == '':
        label['text'] = "Wprowadz numer produktu"
    else:
        result = vending_machine.buy_product(product_id)
        displayed_text = get_displayed_text(result, vending_machine, product_id)
        if result in (vm.BAD_PRODUCT_ID, vm.NOT_ENOUGH_MONEY, vm.STOCK_SHORTAGE):
            show_retry_dialog_window(label, vending_machine, displayed_text)
        else:
            show_transaction_summary(label, vending_machine, displayed_text)


def get_displayed_text(result, vending_machine, product_id):
    switcher = {
        vm.BAD_PRODUCT_ID: "Podaj numer produktu pomiedzy 30 a 50.",
        vm.NOT_ENOUGH_MONEY: "Za malo pieniedzy.",
        vm.STOCK_SHORTAGE: "Produkt niedostepny.",
        vm.BOUGHT_EXACT_CHANGE: f"Kupiles: {vending_machine.find_product_by_id(int(product_id))}",
        vm.UNABLE_TO_GIVE_CHANGE:
            f"Automat nie może wydać reszty.\n"
            f"W celu zakupu proszę umieścić wyliczoną kwotę\n {print_returned_coins(vending_machine.temp_coins)}",
        vm.BOUGHT_RETURNED_CHANGE:
            f"Wydano resztę.\n {print_returned_coins(vending_machine.change)}"
    }
    displayed_text = switcher.get(result, "Invalid result")
    return displayed_text


def print_returned_coins(coins):
    printed_coins = "Zwrócone monety: \n"
    for key, value in coins.items():
        if value > 0:
            if key < 100:
                printed_coins += f"{key}gr: x{value}\n"
            else:
                printed_coins += f"{key/100}zł: x{value}\n"
    return printed_coins


def show_retry_dialog_window(label, vending_machine, displayed_text):
    answer = messagebox.askyesno("Zakup nie powiódł się", f"{displayed_text}\n\nSpróbować ponownie?")
    if not answer:
        label['text'] = print_returned_coins(vending_machine.temp_coins)
        vending_machine.clear_temporary_coin_values()


def show_transaction_summary(label, vending_machine, displayed_text):
    label['text'] = displayed_text
    vending_machine.clear_temporary_coin_values()


def get_coin_buttons(vending_machine, frame_coins, label):
    buttons = []
    for denomination in vm.DENOMINATIONS:
        if denomination < 100:
            buttons.append(tk.Button(frame_coins, text=f"{denomination}gr",
                                     bg='grey', command=lambda d=denomination: insert_coin(vending_machine, label, d)))
        else:
            buttons.append(tk.Button(frame_coins, text=f"{denomination / 100}zl",
                                     bg='grey', command=lambda d=denomination: insert_coin(vending_machine, label, d)))
    return buttons


def place_coin_buttons(buttons):
    relx = COIN_BUTTON_INIT_X
    for button in buttons:
        button.place(relx=relx, rely=COIN_BUTTON_Y, relwidth=COIN_BUTTON_WIDTH, relheight=COIN_BUTTON_HEIGHT)
        relx += 0.11


def get_products():
    return [
        vm.Product(30, "Coca Cola", 220),
        vm.Product(31, "Fanta", 210)
    ]


def main():
    products = get_products()
    vending_machine = vm.VendingMachine(products)

    root = tk.Tk()
    canvas = tk.Canvas(root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()

    frame_coins = tk.Frame(root, bg=FRAME_BG_COLOR, bd=BORDER_SIZE)
    frame_coins.place(relx=FRAME_COINS_X, rely=FRAME_COINS_Y,
                      relwidth=FRAME_COINS_WIDTH, relheight=FRAME_COINS_HEIGHT, anchor='n')

    frame_inserted_value = tk.Frame(root, bg=FRAME_BG_COLOR, bd=BORDER_SIZE)
    frame_inserted_value.place(relx=FRAME_VALUE_X, rely=FRAME_VALUE_Y,
                               relwidth=FRAME_VALUE_WIDTH, relheight=FRAME_VALUE_HEIGHT, anchor='n')

    label = tk.Label(frame_inserted_value)
    label.place(relwidth=LABEL_WIDTH, relheight=LABEL_HEIGHT)

    textbox = tk.Entry(frame_inserted_value, font=40)
    textbox.place(relx=TEXTBOX_X, rely=TEXTBOX_Y,relwidth=TEXTBOX_WIDTH, relheight=TEXTBOX_HEIGHT)

    coin_buttons = get_coin_buttons(vending_machine, frame_coins, label)
    place_coin_buttons(coin_buttons)

    button_buy = tk.Button(frame_inserted_value, text="buy", bg='grey',
                           command=lambda: buy_product(vending_machine, label, textbox.get()))
    button_buy.place(relx=BUY_BUTTON_X, rely=BUY_BUTTON_Y, relwidth=BUY_BUTTON_WIDTH, relheight=BUY_BUTTON_HEIGHT)
    root.mainloop()


if __name__ == '__main__':
    main()
