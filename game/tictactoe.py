
# importing libraries
import tkinter as tk
import json
from threading import Thread
import re
import sys
import socketio
sio = socketio.Client()
url_validity_regex = r"^(((([A-Za-z]{2,5}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)(:[0-9]{1,5})?)$"


class Main():

    def __init__(self):

        # creating tkinter window
        self.win = tk.Tk()
        self.win.title("multiplayer tictactoe")

        self.main_menu_frame = tk.Frame(self.win)
        self.game_frame = tk.Frame(self.win)

        self.url_label = tk.Label(
            self.main_menu_frame, text="Type the url of your partner")
        self.url_entry = tk.Entry(self.main_menu_frame)
        self.url_send_button = tk.Button(
            self.main_menu_frame, text="Post", command=lambda: self.start())

        self.main_menu_frame.grid(row=0, column=0)
        self.url_label.grid(row=0, column=0)
        self.url_entry.grid(row=1, column=0)
        self.url_entry.insert(0, "http://25.46.199.8:2198")
        self.url_send_button.grid(row=2, column=0)

        self.symbol = "P"

        self.url = ""
        self.board = [[], [], []]
        self.board_state = "_________"
        self.goes_first = None
        self.is_first_player = None
        self.local_turn_count = -1
        self.game_end = None
        self.devmode = False
        self.winner = None

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="[_]", borderwidth=1, font=(
                    "Times New Roman", 60), width=3, height=1, command=lambda i=i, j=j: self.click(i, j, self.symbol))
                self.board[i].append(button)
                button.grid(row=i, column=j)

        self.clear_button = tk.Button(
            self.game_frame, text="Replay", command=lambda: self.clear())

        if self.devmode:
            self.clear_button.grid(row=1, column=3)

        self.winner_label = tk.Label(self.game_frame, text="")
        self.winner_label.grid(row=0, column=3)

    @sio.on("debug-events")
    def log_events(data):
        print("debug: ", data)

    def start(self):
        @sio.on("board-state")
        def board_update(board_state):
            board_state = json.loads(board_state)
            print("board_state:", board_state)
            self.winner = board_state.get("winner")
            if self.winner != None:
                self.game_end = True
                if self.winner == self.symbol:
                    self.winner_label.config(text="You win!", fg="#00ff40")
                elif self.winner == "_":
                    self.winner_label.config(text="Draw!", fg="gray")
                else:
                    self.winner_label.config(text="You lose!", fg="red")

            if board_state.get("winner") != None:
                self.clear_button.grid(row=1, column=3)

            if self.local_turn_count != board_state.get("turnCount"):
                temp = self.local_turn_count
                self.local_turn_count = board_state.get("turnCount")
                self.goes_first = True
                print(
                    f"local_turn_count update: {temp}->{self.local_turn_count}")

            self.board_state = board_state.get("boardState")
            for i in range(3):
                for j in range(3):
                    self.board[i][j].config(
                        text=f"[{self.board_state[i*3+j]}]")

            if board_state.get("clear"):
                self.goes_first = None
                self.game_end = False
                print(self.winner_label["text"])
                self.winner_label.config(text="")
                print("text:" + self.winner_label["text"])
                self.update()
                if self.clear_button.winfo_ismapped() and not self.devmode:
                    self.clear_button.grid_forget()

        @sio.on("goes-first")
        def first_player(is_first_player):
            print(is_first_player)
            if is_first_player:
                self.symbol = "X"
                self.is_first_player = True
                self.local_turn_count = 0
            elif not is_first_player:
                self.symbol = "O"
                self.is_first_player = False
                self.local_turn_count = 0
            else:
                print("There was an error while getting the symbol")
        self.url = self.url_entry.get()
        if self.url[len(self.url) - 1] == "/":
            self.url = self.url.rstrip("/")

        # Seeing if the user had done fucked up
        """try:
            self.url_validity_check = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            return print(f"Bad URL schema with url: {self.url}")"""
        try:
            self.thread_server = Thread(self.connect_to_url())
            self.thread_server.start()
            self.thread_server.join()
        except socketio.exceptions.ConnectionError:  # type: ignore
            return print("Connection timeout")

        if not re.match(url_validity_regex, self.url):
            return print("Not the actual website...")

        self.main_menu_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)

        self.update()

    def connect_to_url(self):
        sio.connect(self.url)

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
        print("click(): board_state: " + self.board_state)
        sio.emit("board-state", self.board_state)
        self.goes_first = False
        self.local_turn_count += 1

    def clear(self):
        sio.emit("clear")

    def update(self):
        if self.goes_first == None:
            self.goes_first = self.is_first_player

        if self.local_turn_count < 5 and self.winner_label["text"] != "":
            self.winner_label.config(text="")

        print(
            f"Boardstate: {self.board_state}\nTurncount: {self.local_turn_count}\ncan_click: {self.goes_first}\nwinner: {self.winner}")

    def stop_timer(self):
        sys.exit()


if __name__ == "__main__":
    app = Main()
    app.win.protocol("WM_DELETE_WINDOW", app.stop_timer)
    thread_window = Thread(app.win.mainloop())
    thread_window.start()
    thread_window.join()
