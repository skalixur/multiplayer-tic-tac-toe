# applepie.loca.lt/

# importing libraries
import tkinter as tk
import requests 
import json
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
        button = tk.Button(game_frame, text="[]", borderwidth=1, font=("Times New Roman", 14), width=14, height=7, command=lambda i=i, j=j:click(i, j, symbol))
        board[i].append(button)
        button.grid(row=i, column=j)

get_button = tk.Button(game_frame, text="GET", command=lambda:get())

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
    
    if url[len(url)]== "/":
        url = url.rstrip("/")

    # If the user is smart
    main_menu_frame.grid_forget()
    game_frame.grid(row=0, column=0)
    
def click(row, column, symbol):
    board[row][column]["text"] = f"[{symbol}]"
    board_state[row*3+column] = symbol

    temp = requests.post(url + f"/boardstate?boardstate={board_state}")
    print(temp.text)

def post():
    data = post_entry.get()

    endpoint = ""

    """print(url)
    print(url + endpoint + f"?player1={p1}&player2={p2}")"""

    temp = requests.post(url + f"/?player1={p1}&player2={p2}"+ board_state)
    print(temp.text)

def get():

    data = requests.get(url + "/boardstate")
    data = json.loads(json.loads(data.text))

    print(data.text)

win.mainloop()

