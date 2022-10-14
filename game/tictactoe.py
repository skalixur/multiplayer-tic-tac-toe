import tkinter as tk
import sys
import random

from pkg_resources import ensure_directory

window = tk.Tk()
window.title("TicTacToe")

# Creating variables
player = [
    None,
    None,
]  # both player and bot hold 2 values: [0]:a bool that indicates who is next; [1]: a string containing their symbol
player2 = [None, None]
bot = [None, None]
buttons = []  # stores the buttons on the board
turns = 0
symbols = ["X", "O"]
pNum = 1
# Functions
def checking() -> str:
    """
    This function checks the board every time for 3 matches
    Returns a string if no1's won yet
    """

    # checking for 3 same symbols in a row
    for symbol in symbols:
        # starting from top right corner
        if buttons[0]["text"] == symbol:
            # first row
            if buttons[1]["text"] == symbol:
                if buttons[2]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
            # diagonal from top left to the bottom right
            if buttons[4]["text"] == symbol:
                if buttons[8]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
            # first column
            if buttons[3]["text"] == symbol:
                if buttons[6]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"

        # starting from top right corner
        if buttons[2]["text"] == symbol:
            # diagonal from top right to bottom left
            if buttons[4]["text"] == symbol:
                if buttons[6]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
            # last column
            if buttons[5]["text"] == symbol:
                if buttons[8]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"

        # starting from first row second column
        if buttons[1]["text"] == symbol:
            # diagonal from top right to bottom left
            if buttons[4]["text"] == symbol:
                if buttons[7]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
        # starting from second row first column
        if buttons[3]["text"] == symbol:
            # diagonal from top right to bottom left
            if buttons[4]["text"] == symbol:
                if buttons[5]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
        # starting from third row first column
        if buttons[6]["text"] == symbol:
            # diagonal from top right to bottom left
            if buttons[7]["text"] == symbol:
                if buttons[8]["text"] == symbol:
                    # Someone won
                    if symbol == player[1]:
                        end("player")
                    elif symbol == player2[1]:
                        end("player2")
                    elif symbol == bot[1]:
                        end("bot")
                    else:
                        print("something went wrong...")
                    return "someone won! yeahhhh so happy"
    return "nothing"


def botAlgorithm(b) -> int:
    """
    The bot's thinking of the next move
    Returns the index of the button it wants to click
    """
    # * first it tries to get the middle square
    if buttons[4]["text"] == "":
        return 4

    # * then it checks for avilable places in the corners
    x = 0  # counts the avilable corners
    corners = []  # a list that will contain all free corners
    if buttons[0]["text"] == "":
        x += 1
        corners.append(0)
    if buttons[2]["text"] == "":
        x += 1
        corners.append(2)
    if buttons[6]["text"] == "":
        x += 1
        corners.append(6)
    if buttons[8]["text"] == "":
        x += 1
        corners.append(8)
    if x > 0:
        return int(corners[random.randint(0, x - 1)])

    # * then it just picks a random edge
    for i in range(len(buttons) - 1):
        if buttons[i]["text"] == "" and buttons[i] != b:
            return i


def end(endState):
    """
    Game over
    """
    if endState == "player":
        scoreLabel.config(text="Player 1 won!", fg="green")
    elif endState == "player2":
        scoreLabel.config(text="Player 2 won!", fg="green")
    elif endState == "bot":
        scoreLabel.config(text="Bot won!", fg="red")
    elif endState == "tie":
        scoreLabel.config(text="Tie!", fg="gray")
    else:
        string = (
            "Something somehow went horribly wrong, here's the endState: " + endState
        )
        scoreLabel.config(text=string, fg="black")
    # disable all buttons on board, idk if its needed
    for i in range(9):
        buttons[i]["state"] = "disabled"

    replayLabel.grid(row=0, column=4)
    scoreLabel.grid(row=1, column=4)
    replayButton.grid(row=1, column=3)
    exitButton.grid(row=1, column=5)


def buttonClick(b):
    """
    A button on the board is pressed
    """
    global turns
    # player clicked
    if player[0]:
        # it's a 1 player game
        if player2[0] == None:
            b.config(text=player[1], state="disabled")
            turns += 1

            # if no1 has won yet, check for tie
            # return, if someone has won
            if checking() == "nothing":
                if turns == 9:
                    end("tie")
                    return
            else:
                return
            player[0] = False
            bot[0] = True

            # instantly the bot makes its move
            if checking() == "nothing":
                if turns == 9:
                    end("tie")
                    return
            else:
                return
            buttons[botAlgorithm(b)].invoke()
            player[0] = True
            bot[0] = False

        # it's a 2 player game (so the bot won't make its move instantly after the player)
        else:
            b.config(text=player[1], state="disabled")
            turns += 1
            # if no1 has won yet, check for tie
            # return, if someone has won
            if checking() == "nothing":
                if turns == 9:
                    end("tie")
                    return
            else:
                return
            player[0] = False
            player2[0] = True
            string = (
                f"Player 2 is up next!\nPlayer 1: {player[1]}\nPlayer 2: {player2[1]}"
            )
            trackLabel.config(text=string)
    # player2 clicked
    elif player2[0]:
        b.config(text=player2[1], state="disabled")
        turns += 1
        # if no1 has won yet, check for tie
        # return, if someone has won
        if checking() == "nothing":
            if turns == 9:
                end("tie")
                return
        else:
            return
        player[0] = True
        player2[0] = False
        string = f"Player 1 is up next!\nPlayer 1: {player[1]}\nPlayer 2: {player2[1]}"
        trackLabel.config(text=string)

    # bot clicked
    elif bot[0]:
        b.config(text=bot[1], state="disabled")
        turns += 1
        player[0] = True
        bot[0] = False
        if checking() == "nothing":
            if turns == 9:
                end("tie")
                return
        else:
            return


def start(choice):
    """
    Generates the board
    """
    global turns

    turns = 0
    string = ""  # this will be displayed in trackLabel
    # * 1 player game: player; bot
    if pNum == 1:
        for i in range(2):
            player2[i] = None
        if random.randint(0, 1) == 0:
            player[0] = True
            bot[0] = False
        else:
            player[0] = False
            bot[0] = True

        player[1] = choice
        if choice == "O":
            bot[1] = "X"
        else:
            bot[1] = "O"
        string = f"Player: {player[1]}\nBot: {bot[1]}"
    # * 2 player game: player; player2
    else:
        for i in range(2):
            bot[i] = None
        if random.randint(0, 1) == 0:
            player[0] = True
            player2[0] = False
            string = "Player 1 is up next!"
        else:
            player[0] = False
            player2[0] = True
            string = "Player 2 is up next!"

        player[1] = choice
        if choice == "O":
            player2[1] = "X"
        else:
            player2[1] = "O"
        string += f"\nPlayer 1: {player[1]}\nPlayer 2: {player2[1]}"
    trackLabel.config(text=string)

    """
    COMMENT THE NEXT 2 LINES IF NOT TESTING
    
    player[0] = True
    bot[0] = False
    """

    startFrame.grid_forget()
    gameFrame.grid(row=0, column=0)
    try:
        replayLabel.grid_forget()
        scoreLabel.grid_forget()
        replayButton.grid_forget()
        exitButton.grid_forget()
        for i in range(9):
            buttons[i]["state"] = "normal"
    except:
        pass
    x = 0  # counter for buttons
    for row in range(3):
        for column in range(3):
            buttons[x].grid(row=row, column=column)
            x += 1
    trackLabel.grid(row=3, column=3)
    # if the bot is first, then automatically click a random butotn
    if bot[0]:
        buttons[4].invoke()


def hub():
    """
    Basically the main menu
    """
    if gameFrame.winfo_ismapped():
        for i in range(9):
            buttons[i]["text"] = ""
        gameFrame.grid_forget()
    startFrame.grid(row=0, column=0)
    greetLabel.grid(row=0, column=1)
    xButton.grid(row=1, column=0)
    oButton.grid(row=1, column=2)
    playerNumButton.grid(row=1, column=1)


def playerNumSet():
    global pNum
    if pNum == 2:
        pNum = 1
        playerNumButton.config(text="1 Player", command=lambda: playerNumSet())
    else:
        pNum = 2
        playerNumButton.config(text="2 Players", command=lambda: playerNumSet())


# Creating all the widgets // Main menu
startFrame = tk.Frame(window)
gameFrame = tk.Frame(window)

greetLabel = tk.Label(
    startFrame, text="Welcome to TicTacToe!\n What symbol would you like to be?"
)

xButton = tk.Button(
    startFrame, text="X", width=2, height=1, command=lambda: start(("X"))
)
oButton = tk.Button(
    startFrame, text="O", width=2, height=1, command=lambda: start(("O"))
)
playerNumButton = tk.Button(
    startFrame, text="1 Player", height=1, command=lambda: playerNumSet()
)

# Game
x = 0  # counter for the buttons
for i in range(9):
    buttons.append(
        tk.Button(
            gameFrame,
            text="",
            width=2,
            height=1,
            disabledforeground="black",
            command=lambda x=x: buttonClick(buttons[x]),
        )
    )
    x += 1
trackLabel = tk.Label(
    gameFrame, text=""
)  # displays who is next (when there are 2 players)
# Game over
replayLabel = tk.Label(gameFrame, text="Would you like to play again?")
scoreLabel = tk.Label(gameFrame, text="")
replayButton = tk.Button(
    gameFrame, text="Yes", width=2, height=1, command=lambda: hub()
)
exitButton = tk.Button(
    gameFrame, text="No", width=2, height=1, command=lambda: sys.exit()
)


hub()
window.mainloop()
