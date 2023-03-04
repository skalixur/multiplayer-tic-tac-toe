# I have to rewrite it :C

# importing libraries
import tkinter as tk
import requests 
import json
# creating tkinter window
win = tk.Tk()

post_button = tk.Button(win, text="Post", command=lambda:post())
get_button = tk.Button(win, text="Get", command=lambda:get())
post_entry = tk.Entry(win)
get_entry = tk.Entry(win)

post_button.grid(row=0, column=0)
get_button.grid(row=1, column=0)
post_entry.grid(row=0, column=1)
get_entry.grid(row=1, column=1)
url = "https://applepie.loca.lt/"

def post():
    data = post_entry.get()
    p1 = data[0:data.find(",")]
    p2 = data[data.find(",")+1:len(data)]
    endpoint = "players/players"
    print(url)
    print(url + endpoint + f"?player1={p1}&player2={p2}")
    temp = requests.post(url + endpoint + f"?player1={p1}&player2={p2}")
    print(temp.text)

def get():
    endpoint = "players"

    data = requests.get(url + endpoint + "/")
    data = json.loads(json.loads(data.text))

    get_data = get_entry.get()

    print(data.get(get_data))

win.mainloop()

