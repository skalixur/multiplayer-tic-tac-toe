# applepie.loca.lt/
# http://localhost:6969/

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

symbol = "P"

"""post_button.grid(row=0, column=0)
get_button.grid(row=1, column=0)
post_entry.grid(row=0, column=1)
get_entry.grid(row=1, column=1)"""

url = ""
board=[[],[],[]]
board_state = "_________"
can_click = None
is_first_player = None
local_turn_count = -1


for i in range(3):
    for j in range(3):
        button = tk.Button(game_frame, text="[_]", borderwidth=1, font=("Times New Roman", 14), width=14, height=7, command=lambda i=i, j=j:click(i, j, symbol))
        board[i].append(button)
        button.grid(row=i, column=j)

get_button = tk.Button(game_frame, text="GET", command=lambda:update())
get_button.grid(row=0, column=3)
clear_button = tk.Button(game_frame, text="CLEAR", command=lambda:clear())
clear_button.grid(row=1, column=3)

                  
def start():
    global url, symbol, can_click, is_first_player, local_turn_count
    url = url_entry.get()

    if url[len(url) - 1]== "/":
        url = url.rstrip("/")

    # Seeing if the user had done fucked up
    try:
        url_validity_check = requests.get(url)
    except requests.exceptions.MissingSchema:
        return print(f"Invalid URL: {url}")
    url_validity_check = json.loads(requests.get(url + "/isfirstplayer").text)
    print(url_validity_check)
    if url_validity_check.get("isFirstPlayer"):
        symbol = "X"
        is_first_player = True
        local_turn_count = 0
    elif not url_validity_check.get("isFirstPlayer"):
        symbol = "O"
        is_first_player = False
        local_turn_count = 0
    else:
        print("There was an error while getting the symbol")

    if url_validity_check.get("statusCode") != 200:
        return print("Not the actual website...")
    

    # If the user is smart
    main_menu_frame.grid_forget()
    game_frame.grid(row=0, column=0)
    
def click(row, column, symbol):
    global board_state, can_click, local_turn_count

    if board[row][column]["text"] != "[_]" or not can_click:
        return

    board[row][column].config(text=f"[{symbol}]")

    temp = []
    for i in board_state:
        temp.append(i)
    temp[row*3+column] = symbol
    board_state = ""
    for i in temp:
        board_state += i

    temp = requests.post(url + f"/boardstate?boardstate=bs:{board_state}")
    print(temp.text)
    can_click = False
    local_turn_count += 1

def clear():
    temp = requests.post(url + f"/clear")
    print(temp.text)


def update():
    global board, board_state, local_turn_count, can_click

    data = json.loads(requests.get(url + "/boardstate").text)

    if local_turn_count != data.get("turnCount"):
        local_turn_count = data.get("turnCount")
        can_click = True
    
    if can_click == None:
        can_click = json.loads(requests.get(url + "/isfirstplayer").text).get("firstPlayer")

    data = re.sub(r'.', '', data.get("boardState"), count = 3)
    board_state = data

    for i in range(3):
        for j in range(3):
            board[i][j].config(text=f"[{board_state[i*3+j]}]")
    
    print(f"Boardstate: {board_state}\nTurncount: {local_turn_count}\n")
            

win.mainloop()