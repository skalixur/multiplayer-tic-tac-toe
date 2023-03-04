# I have to rewrite it :C

# importing libraries
import tkinter as tk
import requests
import json

# creating tkinter window
win = tk.Tk()

post_button = tk.Button(win, text="Post", command=lambda:post())
get_button = tk.Button(win, text="Get", command=lambda:get())
post_label = tk.Label(win, text="Post: ")
get_label = tk.Label(win, text="Get: ")
post_entry = tk.Entry(win)
get_entry = tk.Entry(win)

post_button.grid(row=0, column=0)
get_button.grid(row=1, column=0)
post_label.grid(row=0, column=1)
get_label.grid(row=1, column=1)
post_entry.grid(row=0, column=2)
get_entry.grid(row=1, column=2)


def post():
    url = "http://localhost:6969/"
    p1 = "p1"
    p2 = "p2"
    endpoint = "players/players"
    url = url + endpoint + f"?player1={p1}&player2={p2}"
    temp = requests.post(url)
    print(temp.text)

def get():
    url = "http://localhost:6969/"
    endpoint = "players"

    url = url + endpoint + "/"
    data = requests.get(url)
    data = json.loads(json.loads(data.text))
    print(data.get("player1"))

win.mainloop()

