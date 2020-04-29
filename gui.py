from vending_machine import VendingMachine, Coin, Product
import tkinter as tk

HEIGHT = 500
WIDTH = 600


def insert_coin(val):
    vending_machine.insert_coin(val)
    if vending_machine.inserted_money < 100:
        label['text'] = "Wplaciles: " + str(vending_machine.inserted_money) + "gr"
    else:
        label['text'] = "Wplaciles: " + str(int(vending_machine.inserted_money / 100)) + "zl " \
                        + str(vending_machine.inserted_money % 100) + "gr"


def buy_product(product_id):
    label['text'] = vending_machine.buy_product(product_id)


root = tk.Tk()
vending_machine = VendingMachine()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame_coins = tk.Frame(root, bg='#9c978a', bd=5)
frame_coins.place(relx=0.5, rely=0.05, relwidth=0.90, relheight=0.1, anchor='n')

button_1 = tk.Button(frame_coins, text="1gr", bg='grey', command=lambda: insert_coin(1))
button_1.place(relx=0.01, rely=0.25, relwidth=0.1, relheight=0.5)

button_2 = tk.Button(frame_coins, text="2gr", bg='grey', command=lambda: insert_coin(2))
button_2.place(relx=0.12, rely=0.25, relwidth=0.1, relheight=0.5)

button_5 = tk.Button(frame_coins, text="5gr", bg='grey', command=lambda: insert_coin(5))
button_5.place(relx=0.23, rely=0.25, relwidth=0.1, relheight=0.5)

button_10 = tk.Button(frame_coins, text="10gr", bg='grey', command=lambda: insert_coin(10))
button_10.place(relx=0.34, rely=0.25, relwidth=0.1, relheight=0.5)

button_20 = tk.Button(frame_coins, text="20gr", bg='grey', command=lambda: insert_coin(20))
button_20.place(relx=0.45, rely=0.25, relwidth=0.1, relheight=0.5)

button_50 = tk.Button(frame_coins, text="50gr", bg='grey', command=lambda: insert_coin(50))
button_50.place(relx=0.56, rely=0.25, relwidth=0.1, relheight=0.5)

button_100 = tk.Button(frame_coins, text="1zl", bg='grey', command=lambda: insert_coin(100))
button_100.place(relx=0.67, rely=0.25, relwidth=0.1, relheight=0.5)

button_200 = tk.Button(frame_coins, text="2zl", bg='grey', command=lambda: insert_coin(200))
button_200.place(relx=0.78, rely=0.25, relwidth=0.1, relheight=0.5)

button_500 = tk.Button(frame_coins, text="5zl", bg='grey', command=lambda: insert_coin(500))
button_500.place(relx=0.89, rely=0.25, relwidth=0.1, relheight=0.5)

frame_inserted_value = tk.Frame(root, bg='#9c978a', bd=5)
frame_inserted_value.place(relx=0.5, rely=0.17, relwidth=0.90, relheight=0.1, anchor='n')

label = tk.Label(frame_inserted_value)
label.place(relwidth=0.4, relheight=1)

textbox = tk.Entry(frame_inserted_value, font=40)
textbox.place(relx=0.45, relwidth=0.3, relheight=1)

button_buy = tk.Button(frame_inserted_value, text="buy", bg='grey',
                       command=lambda: buy_product(textbox.get()))
button_buy.place(relx=0.80, rely=0.2, relwidth=0.1, relheight=0.5)
root.mainloop()
