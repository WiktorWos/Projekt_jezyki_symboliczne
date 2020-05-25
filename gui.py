import vending_machine as vm
import tkinter as tk

CANVAS_HEIGHT, CANVAS_WIDTH = 500, 600
FRAME_BG_COLOR = '#9c978a'
BORDER_SIZE = 5
FRAME_COINS_X, FRAME_COINS_Y, FRAME_COINS_WIDTH, FRAME_COINS_HEIGHT = 0.5, 0.05, 0.9, 0.1
FRAME_VALUE_X, FRAME_VALUE_Y, FRAME_VALUE_WIDTH, FRAME_VALUE_HEIGHT = 0.5, 0.17, 0.9, 0.1
LABEL_WIDTH, LABEL_HEIGHT = 0.4, 1
TEXTBOX_X, TEXTBOX_WIDTH, TEXTBOX_HEIGHT = 0.45, 0.3, 1
COIN_BUTTON_INIT_X, COIN_BUTTON_Y, COIN_BUTTON_WIDTH, COIN_BUTTON_HEIGHT = 0.01, 0.25, 0.1, 0.5
BUY_BUTTON_X, BUY_BUTTON_Y, BUY_BUTTON_WIDTH, BUY_BUTTON_HEIGHT = 0.8, 0.2, 0.1, 0.5


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
        switcher = {
            vm.BAD_PRODUCT_ID: "Podaj numer produktu pomiedzy 30 a 50",
            vm.NOT_ENOUGH_MONEY: "Za malo pieniedzy",
            vm.STOCK_SHORTAGE: "Produkt niedostepny",
            vm.BOUGHT: f"Kupiles: {vending_machine.find_product_by_id(int(product_id))}"
        }
        result = vending_machine.buy_product(product_id)
        label['text'] = switcher.get(result, "Invalid result")


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
    textbox.place(relx=TEXTBOX_X, relwidth=TEXTBOX_WIDTH, relheight=TEXTBOX_HEIGHT)

    coin_buttons = get_coin_buttons(vending_machine, frame_coins, label)
    place_coin_buttons(coin_buttons)

    button_buy = tk.Button(frame_inserted_value, text="buy", bg='grey',
                           command=lambda: buy_product(vending_machine, label, textbox.get()))
    button_buy.place(relx=BUY_BUTTON_X, rely=BUY_BUTTON_Y, relwidth=BUY_BUTTON_WIDTH, relheight=BUY_BUTTON_HEIGHT)
    root.mainloop()


if __name__ == '__main__':
    main()
