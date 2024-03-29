# http://localhost:6969

# importing libraries
import tkinter as tk
import json
from threading import Thread
import re
import socketio
import os
import config
import random

sio = socketio.Client()
url_validity_regex = r"^(((([A-Za-z]{2,5}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)(:[0-9]{1,5})?)$"
devmode = True

random_usernames = config.data.get("random_usernames")
button_font = config.data.get("button_font")
label_font = config.data.get("label_font")
max_username_length = config.data.get("max_username_length")


class Main():
    def __init__(self):

        self.own_symbol = "P"
        self.other_symbol = "PP"
        self.url = ""
        self.board = [[], [], []]
        self.board_state = "_________"
        self.goes_first = None
        self.is_first_player = None
        self.local_turn_count = -1
        self.game_end = None
        self.winner = None
        self.received_goes_first = False
        self.own_username = "##1234567890123456##"
        self.other_username = "###1234567890123456###"

        # creating tkinter window
        self.win = tk.Tk()
        self.win.title("multiplayer tictactoe")

        # creating frames
        self.main_menu_frame = tk.Frame(self.win)
        self.game_frame = tk.Frame(self.win)

        # widgets in main_menu_frame
        self.url_label = tk.Label(
            self.main_menu_frame, text="Type the url of your partner")
        self.url_entry = tk.Entry(self.main_menu_frame)
        self.url_label = tk.Label(self.main_menu_frame, text="URL:")
        self.username_entry = tk.Entry(self.main_menu_frame)
        self.username_label = tk.Label(self.main_menu_frame, text="Username:")
        self.url_send_button = tk.Button(
            self.main_menu_frame, text="Connect", command=lambda: self.start())

        self.main_menu_frame.grid(row=0, column=0)
        self.url_label.grid(row=0, column=0)
        self.url_entry.grid(row=0, column=1)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.url_entry.insert(0, "http://25.46.199.8:2198")
        self.url_send_button.grid(row=3, column=0, columnspan=2)

        # widgets in game_frame
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="[_]", borderwidth=1, font=button_font, width=3,
                                   height=1, command=lambda i=i, j=j: self.click(i, j, self.own_symbol))
                self.board[i].append(button)
                button.grid(row=i+1, column=j)

        self.clear_button = tk.Button(
            self.game_frame, text="Replay", command=lambda: self.clear())

        self.own_username_display_label = tk.Label(self.game_frame)
        self.score_label = tk.Label(
            self.game_frame, text="0 - 0", font=("Times New Roman", 20))
        self.other_username_display_label = tk.Label(self.game_frame)
        self.winner_label = tk.Label(self.game_frame)

        self.own_username_display_label.grid(row=0, column=0,)
        self.score_label.grid(row=0, column=1)
        self.other_username_display_label.grid(row=0, column=2)
        self.winner_label.grid(row=0, column=3)

        if devmode:
            self.clear_button.grid(row=1, column=3)

    @sio.on("debug-events")
    def log_events(data):
        print("debug: ", data)

    def label_boldyfier(self, label, doit):
        if doit:
            font = list(label_font)
            font.append("bold")
            label.config(
                font=tuple(font))
        else:
            label.config(font=label_font)

    def start(self):
        @sio.on("board-state")
        def board_update(board_state):
            board_state = json.loads(board_state)
            print("board_state:", board_state)
            self.winner = board_state.get("winner")
            if self.winner != None:
                self.game_end = True
                if self.winner == self.own_symbol:
                    self.winner_label.config(text="You win!", fg="#00ff40")
                elif self.winner == self.other_symbol:
                    self.winner_label.config(text="You lose!", fg="red")
                elif self.winner == "_":
                    self.winner_label.config(text="Draw!", fg="gray")
                else:
                    return print("There was an error in board_update()")
                player_1_score = board_state.get("player1Score")
                player_2_score = board_state.get("player2Score")

                score = ""
                if self.is_first_player:
                    score = f"{player_1_score} - {player_2_score}"
                else:
                    score = f"{player_2_score} - {player_1_score}"

                if score != "":
                    self.score_label["text"] = score
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
                if self.clear_button.winfo_ismapped() and not devmode:
                    self.clear_button.grid_forget()
                self.received_goes_first = False

            if self.goes_first:
                print("********\nother no\nme yes\n********")
                # remove highlight other player's username
                self.label_boldyfier(self.other_username_display_label, False)

                # highlight own username
                self.label_boldyfier(self.own_username_display_label, True)

        @ sio.on("goes-first")
        def first_player(is_first_player):
            print("isfistplayer is: ", is_first_player)
            if is_first_player:
                self.own_symbol = "X"
                self.other_symbol = "O"
                self.is_first_player = True
                self.local_turn_count = 0

                print("********\nme yes\n********")
                # highlight own username
                self.label_boldyfier(self.own_username_display_label, True)

            elif not is_first_player:
                self.own_symbol = "O"
                self.other_symbol = "X"
                self.is_first_player = False
                self.local_turn_count = 0

                print("********\nother yes\n********")
                # highlight other username
                self.label_boldyfier(self.other_username_display_label, True)
            else:
                print("There was an error while getting the symbol")
            self.received_goes_first = True

            # handling username
            if self.username_entry.get() != "":
                self.own_username = self.username_entry.get()
            else:
                while len(self.own_username) > 16:
                    self.own_username = random_usernames[random.randint(
                        0, len(random_usernames) - 1)] + str(random.randint(0, 999))
            if self.is_first_player:
                sio.emit("setplayers", {"player": 1,
                         "playerName": self.own_username})
            else:
                sio.emit("setplayers", {"player": 2,
                         "playerName": self.own_username})

            temp = f"{self.own_symbol} - {self.own_username} (You)"
            self.own_username_display_label.config(text=temp)

            self.update()

        @ sio.on("playernames")
        def receive_player_names(data):
            if self.is_first_player:
                self.other_username = data.get("player2Name")
            else:
                self.other_username = data.get("player1Name")

            if self.other_username != "":
                temp = f"{self.other_symbol} - {self.other_username} (Them)"
                self.other_username_display_label.config(text=temp)

        self.url = self.url_entry.get()
        if self.url[len(self.url) - 1] == "/":
            self.url = self.url.rstrip("/")

        if len(self.username_entry.get()) > max_username_length:
            return print(f"Too long username! (max: {max_username_length})")

        # Seeing if the user had done fucked up
        try:
            self.thread_server = Thread(self.connect_to_url())
            self.thread_server.start()
            self.thread_server.join()
        except socketio.exceptions.ConnectionError:  # type: ignore
            return print("Connection timeout")

        if not re.match(url_validity_regex, self.url):
            return print("Bad URL schema!")

        self.main_menu_frame.grid_forget()
        self.game_frame.grid(row=0, column=0)

        self.update()

    def connect_to_url(self):
        sio.connect(self.url)

    def click(self, row, column, symbol):

        if (self.board[row][column]["text"] != "[_]" or not self.goes_first or self.game_end) and not devmode:
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

        print("********\nother yes\nme no\n********")
        # highlight other player's username
        self.label_boldyfier(self.other_username_display_label, True)

        # remove highlight own username
        self.label_boldyfier(self.own_username_display_label, False)

    def clear(self):
        sio.emit("clear", {"clearScore": True})

    def update(self):
        if self.goes_first == None and self.received_goes_first:
            self.goes_first = self.is_first_player
        else:
            return

        if self.local_turn_count < 5 and self.winner_label["text"] != "":
            self.winner_label.config(text="")

        print(
            f"Boardstate : {self.board_state}\nTurncount  : {self.local_turn_count}\ncan_click  : {self.goes_first}\nwinner     : {self.winner}")

    def stop_timer(self):
        os._exit(0)


if __name__ == "__main__":
    app = Main()
    app.win.protocol("WM_DELETE_WINDOW", app.stop_timer)
    thread_window = Thread(app.win.mainloop())
    thread_window.start()
    thread_window.join()
