# applepie.loca.lt/
# http://localhost:6969/

# importing libraries
import tkinter as tk
import requests 
import json
from threading import Timer
import time
import re
import sys
import traceback

class Main():

    def __init__(self):

        # creating tkinter window
        self.win = tk.Tk()
        self.win.title("multiplayer tictactoe")

        self.main_menu_frame = tk.Frame(self.win)
        self.game_frame = tk.Frame(self.win)

        self.url_label = tk.Label(self.main_menu_frame, text="Type the url of your partner")
        self.url_entry = tk.Entry(self.main_menu_frame)
        self.url_send_button = tk.Button(self.main_menu_frame, text="Post", command=lambda:self.start())

        self.main_menu_frame.grid(row=0, column=0)
        self.url_label.grid(row=0, column=0)
        self.url_entry.grid(row=1, column=0)
        self.url_entry.insert(0, "https://applepie.loca.lt/")
        self.url_send_button.grid(row=2, column=0)

        self.symbol = "P"

        self.url = ""
        self.board=[[],[],[]]
        self.board_state = "_________"
        self.goes_first = None
        self.is_first_player = None
        self.local_turn_count = -1
        self.game_end = None
        self.devmode = False
        self.winner = None

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="[_]", borderwidth=1, font=("Times New Roman", 60), width=3, height=1, command=lambda i=i, j=j:self.click(i, j, self.symbol))
                self.board[i].append(button)
                button.grid(row=i, column=j)

        self.clear_button = tk.Button(self.game_frame, text="CLEAR", command=lambda:self.clear())
        self.clear_button.grid(row=1, column=3)
        self.winner_label = tk.Label(self.game_frame, text="")
        self.winner_label.grid(row=0, column=3)
                    
    def start(self):
        self.url = self.url_entry.get()
        if self.url[len(self.url) - 1]== "/":
            self.url = self.url.rstrip("/")

        # Seeing if the user had done fucked up
        try:
            self.url_validity_check = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            return print(f"Bad URL schema with url: {self.url}")
        if str(self.url_validity_check.text) == "404":
            return print(f"Couldn't connect to url: {self.url}\nMaybe it's not online?")
        
        self.update_timer = RepeatTimer(1, self.update)
        self.update_timer.start()

        self.url_validity_check = json.loads(requests.get(self.url + "/isfirstplayer").text)
        print(self.url_validity_check)
        if self.url_validity_check.get("goesFirst"):
            self.symbol = "X"
            self.is_first_player = True
            self.local_turn_count = 0
        elif not self.url_validity_check.get("goesFirst"):
            self.symbol = "O"
            self.is_first_player = False
            self.local_turn_count = 0
        else:
            print("There was an error while getting the symbol")

        if self.url_validity_check.get("statusCode") != 200:
            return print("Not the actual website...")

        self.main_menu_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)
        
        self.update()

    def click(self, row, column, symbol):

        if (self.board[row][column]["text"] != "[_]" or not self.goes_first or self.game_end) and not self.devmode:
            return

        self.board[row][column].config(text=f"[{symbol}]")

        temp = []
        for i in self.board_state:
            temp.append(i)
        temp[row*3+column] = symbol
        self.board_state = ""
        for i in temp:
            self.board_state += i

        temp = requests.post(self.url + f"/boardstate?boardstate=bs:{self.board_state}")
        print(temp.text)
        self.goes_first = False
        self.local_turn_count += 1


    def clear(self):
        temp = requests.post(self.url + f"/clear")
        self.goes_first = None
        self.game_end = False
        self.winner_label["text"] = ""
        self.update()
        print(temp.text)


    def check_rows(self):
        for i in self.board_state:
            pass

    def update(self):
        if self.goes_first == None:
            self.goes_first = self.is_first_player

        data = json.loads(requests.get(self.url + "/boardstate").text)

        self.winner = data.get("winner")
        if self.winner != None:
            self.game_end = True
            if self.winner == self.symbol:
                self.winner_label.config(text="You win!", fg="#00ff40")
            elif self.winner == "_":
                self.winner_label.config(text="Draw!", fg="gray")
            else:
                self.winner_label.config(text="You lose!", fg="red")
        if self.local_turn_count != data.get("turnCount"):
            temp = self.local_turn_count
            self.local_turn_count = data.get("turnCount")
            self.goes_first = True

            print(f"local_turn_count update: {temp}->{self.local_turn_count}")
        
        data = re.sub(r'.', '', data.get("boardState"), count = 3)
        self.board_state = data

        for i in range(3):
            for j in range(3):
                self.board[i][j].config(text=f"[{self.board_state[i*3+j]}]")
        
        if self.local_turn_count < 5 and self.winner_label["text"] != "":
            self.winner_label.config(text="")
        print(f"Boardstate: {self.board_state}\nTurncount: {self.local_turn_count}\ncan_click: {self.goes_first}\nwinner: {self.winner}")

    def stop_timer(self):
        try:
            self.update_timer.cancel()
        except AttributeError: # If the timer was already stopped
            pass

        sys.exit()
    
class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  

if __name__ == "__main__":
    app = Main()
    app.win.protocol("WM_DELETE_WINDOW", app.stop_timer)
    app.win.mainloop()