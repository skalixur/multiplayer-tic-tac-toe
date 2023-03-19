# http://localhost:6969

# importing libraries
import tkinter as tk
from threading import Thread
import json
import re
import socketio
import os
import config
import random
import time

sio = socketio.Client()
url_validity_regex = r"^(((([A-Za-z]{2,5}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)(:[0-9]{1,5})?)$"
devmode = False
random.seed(time.time())

random_usernames = config.data.get("random_usernames")
button_font = config.data.get("button_font")
label_font = config.data.get("label_font")
max_username_length = config.data.get("max_username_length")


class Main():
    def __init__(self):

        self.own_symbol = "P"
        self.other_symbol = "PP"
        self.board_state = "_________"
        self.goes_first = None
        self.is_first_player = None
        self.local_turn_count = -1
        self.game_end = None
        self.winner = None
        self.received_goes_first = False
        self.own_username = "##1234567890123456##"
        self.other_username = "###1234567890123456###"
        self.true_first_player = None
        self.in_server = False

        # creating tkinter window
        self.win = tk.Tk()
        self.win.title("multiplayer tictactoe")

        # creating frames
        self.main_menu_frame = tk.Frame(self.win)

        # widgets in main_menu_frame
        self.url_label = tk.Label(
            self.main_menu_frame, text="Type the url of your partner")
        self.url_entry = tk.Entry(self.main_menu_frame)
        self.url_label = tk.Label(self.main_menu_frame, text="URL:")
        self.username_entry = tk.Entry(self.main_menu_frame)
        self.username_label = tk.Label(self.main_menu_frame, text="Username:")
        self.url_send_button = tk.Button(
            self.main_menu_frame, text="Connect", command=lambda: self.connect_press())

        self.main_menu_frame.grid(row=0, column=0)
        self.url_label.grid(row=0, column=0)
        self.url_entry.grid(row=0, column=1)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.url_entry.insert(0, "http://localhost:6969")
        self.url_send_button.grid(row=3, column=0, columnspan=2)

        self.set_game_frame_widgers()

    def set_game_frame_widgers(self):
        self.game_frame = tk.Frame(self.win)
        self.board = [[], [], []]

        if button_font is not None:
            for i in range(3):
                for j in range(3):
                    button = tk.Button(self.game_frame, text="[_]", borderwidth=1, font=button_font, width=3,
                                       height=1, command=lambda i=i, j=j: self.click(i, j, self.own_symbol))
                    self.board[i].append(button)
                    button.grid(row=i+1, column=j)
        else:
            print("button_font is None!")

        self.clear_button = tk.Button(
            self.game_frame, text="Replay", command=lambda: self.clear())

        self.own_username_display_label = tk.Label(self.game_frame)
        self.score_label = tk.Label(
            self.game_frame, text="0 - 0", font=("Times New Roman", 20))
        self.other_username_display_label = tk.Label(self.game_frame)
        self.winner_label = tk.Label(self.game_frame)
        self.disconnect_button = tk.Button(
            self.game_frame, text="Disconnect", command=lambda: self.disconnect())

        self.own_username_display_label.grid(row=0, column=0,)
        self.score_label.grid(row=0, column=1)
        self.other_username_display_label.grid(row=0, column=2)
        self.winner_label.grid(row=0, column=3)
        self.disconnect_button.grid(row=3, column=3)

        if devmode:
            self.clear_button.grid(row=1, column=3)

    def disconnect(self):
        print("Disconnecting...")
        sio.emit("clear", {"clearScore": True})
        if self.in_server:
            self.in_server = False
            sio.disconnect()
        elif not self.in_server:
            return
        self.true_first_player = None
        self.own_username = "##1234567890123456##"
        self.game_frame.destroy()
        self.main_menu_frame.grid(row=0, column=0)
        print("Disconnected!")

    def label_boldyfier(self, label, doit):
        if doit and label_font is not None:
            font = list(label_font)
            font.append("bold")
            label.config(
                font=tuple(font))
        else:
            label.config(font=label_font)

    def connect_press(self):
        @ sio.on("goes-first")  # type: ignore
        def first_player(is_first_player):
            if self.in_server:
                print("isfistplayer is: ", is_first_player)
                self.goes_first = is_first_player
                if self.true_first_player is None:
                    self.true_first_player = is_first_player
                old_symbol = self.own_symbol
                switch = ""

                if is_first_player:
                    self.own_symbol = "X"
                    self.other_symbol = "O"
                    self.is_first_player = True
                    self.local_turn_count = 0

                elif not is_first_player:
                    self.own_symbol = "O"
                    self.other_symbol = "X"
                    self.is_first_player = False
                    self.local_turn_count = 0

                else:
                    print("There was an error while getting first_player")
                self.received_goes_first = True

                # handling username
                if random_usernames is not None:
                    if self.username_entry.get() != "":
                        self.own_username = self.username_entry.get()
                    else:
                        while len(self.own_username) > 16:
                            self.own_username = random_usernames[random.randint(
                                0, len(random_usernames) - 1)] + str(random.randint(0, 999))
                else:
                    print("random_username is None!")

                if self.true_first_player:
                    sio.emit("setplayers", {"player": 1,
                                            "playerName": self.own_username, "playerSymbol": self.own_symbol})
                elif not self.true_first_player:
                    sio.emit("setplayers", {"player": 2,
                                            "playerName": self.own_username, "playerSymbol": self.own_symbol})

                temp = f"{self.own_symbol} - {self.own_username} (You)"
                self.own_username_display_label.config(text=temp)

                # highlight own username and other's username
                self.label_boldyfier(
                    self.own_username_display_label, self.is_first_player)
                self.label_boldyfier(
                    self.other_username_display_label, not self.is_first_player)

        @sio.on("board-state")  # type: ignore
        def board_update(board_state):
            if self.in_server:
                board_state = json.loads(board_state)
                print("board_state:", board_state)
                self.winner = board_state.get("winner")
                if self.winner is not None:
                    self.game_end = True
                    if self.winner == self.own_symbol:
                        self.winner_label.config(text="You win!", fg="#00ff40")
                    elif self.winner == self.other_symbol:
                        self.winner_label.config(text="You lose!", fg="red")
                    elif self.winner == "_":
                        self.winner_label.config(text="Draw!", fg="gray")
                    else:
                        return print("There was an error in board_update()")

                    player_1_score = board_state.get("player1")["score"]
                    player_2_score = board_state.get("player2")["score"]

                    score = "",

                    if self.true_first_player:
                        score = f"{player_1_score} - {player_2_score}"
                    elif not self.true_first_player:
                        score = f"{player_2_score} - {player_1_score}"

                    if score != "":
                        self.score_label["text"] = score
                if board_state.get("winner") is not None:
                    self.clear_button.grid(row=1, column=3)

                if self.local_turn_count != board_state.get("turnCount"):
                    new_turn_count = board_state.get("turnCount")
                    old_local_turncount = self.local_turn_count
                    if new_turn_count != 0:
                        self.goes_first = True
                    self.local_turn_count = new_turn_count
                    print(
                        f"local_turn_count update: {old_local_turncount}->{self.local_turn_count}")

                self.board_state = board_state.get("boardState")
                for i in range(3):
                    for j in range(3):
                        self.board[i][j].config(
                            text=f"[{self.board_state[i*3+j]}]")

                if board_state.get("clear"):
                    self.received_goes_first = False
                    self.game_end = False
                    self.winner_label.config(text="")
                    self.print_state()
                    if self.clear_button.winfo_ismapped() and not devmode:
                        self.clear_button.grid_forget()

                if self.goes_first:
                    # print("********\nother no\nme yes\n********")
                    # remove highlight other player's username
                    self.label_boldyfier(
                        self.other_username_display_label, False)

                    # highlight own username
                    self.label_boldyfier(self.own_username_display_label, True)

                self.print_state()

        @ sio.on("players")  # type: ignore
        def receive_player_names(data):
            if self.is_first_player:
                self.other_username = data.get("player2")["name"]
            elif not self.is_first_player:
                self.other_username = data.get("player1")["name"]
            else:
                print("in receive_player_names() error")

            # need to remove the :{symbol} at the end of the name
            self.other_username = self.other_username[:-2]

            if self.other_username != "":
                temp = f"{self.other_symbol} - {self.other_username} (Them)"
                self.other_username_display_label.config(text=temp)

        @sio.on("disconn")  # type: ignore
        def on_disconnect():
            self.disconnect()

        #! connect_press() starts here

        # getting the url
        self.url = self.url_entry.get()
        if self.url[len(self.url) - 1] == "/":
            self.url = self.url.rstrip("/")

        # checking username
        if max_username_length is not None:
            if len(self.username_entry.get()) > max_username_length:
                return print(f"Too long username! (max: {max_username_length})")
        if self.username_entry.get().find(":") != -1:
            return print("Username can't contain the \':\' character.")

        # Trying to connect to url
        try:
            if not self.game_frame.winfo_exists():
                self.set_game_frame_widgers()
            self.thread_server = Thread(self.connect_to_url())
            self.thread_server.start()
            self.thread_server.join()
        except socketio.exceptions.ConnectionError:  # type: ignore
            self.in_server = False
            return print("Connection timeout", self.url)

        if not re.match(url_validity_regex, self.url):
            return print("Bad URL schema!")

        while True:
            if self.is_first_player is not None:
                # showing game
                self.game_frame.grid(row=0, column=0)
                self.main_menu_frame.grid_forget()

                self.print_state()
                break

    def connect_to_url(self):
        self.in_server = True
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
        sio.emit("board-state", self.board_state)
        self.goes_first = False
        self.local_turn_count += 1

        # print("********\nother yes\nme no\n********")
        # highlight other player's username
        self.label_boldyfier(self.other_username_display_label, True)

        # remove highlight own username
        self.label_boldyfier(self.own_username_display_label, False)

    def clear(self):
        sio.emit("clear", {"clearScore": False})

    def print_state(self):
        print(
            f"\ntruefirst       : {self.true_first_player}\nBoardstate      : {self.board_state}\nTurncount       : {self.local_turn_count}\ncan_click       : {self.goes_first}\nwinner          : {self.winner}\nsymbol          : {self.own_symbol}\nis_first_player : {self.is_first_player}\n")

    def stop_timer(self):
        os._exit(0)


if __name__ == "__main__":
    app = Main()
    app.win.protocol("WM_DELETE_WINDOW", app.stop_timer)
    thread_window = Thread(app.win.mainloop())
    thread_window.start()
    thread_window.join()
