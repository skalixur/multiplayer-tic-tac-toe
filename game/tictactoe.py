# applepie.loca.lt/

# importing libraries
import tkinter as tk
import requests 
import json
import threading
import time
import re

# creating tkinter window
win = tk.Tk()

main_menu_frame = tk.Frame(win)
game_frame = tk.Frame(win)

url_label = tk.Label(main_menu_frame, text="Type the url of your partner")
url_entry = tk.Entry(main_menu_frame)
url_send_button = tk.Button(main_menu_frame, text="Post", command=lambda:start())

main_menu_frame.grid(row=0, column=0)
url_label.grid(row=0, column=0)
url_entry.grid(row=1, column=0)
url_entry.insert(0, "https://applepie.loca.lt/")
url_send_button.grid(row=2, column=0)

symbol = "O"

"""post_button.grid(row=0, column=0)
get_button.grid(row=1, column=0)
post_entry.grid(row=0, column=1)
get_entry.grid(row=1, column=1)"""

url = ""
board=[[],[],[]]
board_state = "_________"

for i in range(3):
    for j in range(3):
        button = tk.Button(game_frame, text="[_]", borderwidth=1, font=("Times New Roman", 14), width=14, height=7, command=lambda i=i, j=j:click(i, j, symbol))
        board[i].append(button)
        button.grid(row=i, column=j)

get_button = tk.Button(game_frame, text="GET", command=lambda:update())
get_button.grid(row=0, column=3)

def start():
    global url
    url = url_entry.get()

    # Seeing if the user had done fucked up
    try:
        url_validity_check = requests.get(url)
    except requests.exceptions.MissingSchema:
        return print(f"Invalid URL: {url}")
    url_validity_check = requests.get(url + "/isfirstplayer")
    if not url_validity_check:
        return print("Not the actual website...")
    
    if url[len(url) - 1]== "/":
        url = url.rstrip("/")

    # If the user is smart
    main_menu_frame.grid_forget()
    game_frame.grid(row=0, column=0)
    
def click(row, column, symbol):
    global board_state

    board[row][column]["text"] = f"[{symbol}]"

    temp = []
    for i in board_state:
        temp.append(i)
    temp[row*3+column] = symbol
    board_state = ""
    for i in temp:
        board_state += i

    temp = requests.post(url + f"/boardstate?boardstate=bs:{board_state}")
    print(temp.text)



def update():
    global board, board_state

    data = requests.get(url + "/boardstate")
    data = json.loads(data.text).get('boardState')

    data = re.sub(r'.', '', data, count = 3)
    board_state = data
    # data indexing thing has a +3 after it because it starts with "bs:" and we dont need that shit"
    for i in range(3):
        for j in range(3):
            board[i][j].config(text=f"[{data[i*3+j]}]")
            

win.mainloop()

