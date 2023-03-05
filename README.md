# Multiplayer tic tac toe

Multiplayer tic tac toe collaboration with @[ricsirogi](https://github.com/ricsirogi)

# how it works

both clients connect to the server, and afterwards the server responds with whether or not you go first. the validation of the server also happens in this stage. after that, the clients both repeatedly GET the boardstate from the server every 1s (very inefficient, i know) when a player clicks on a button, the updated boardstate is POSTed to the server. (yes, this makes it incredibly easy to cheat) The server then validates the board state, uses regex to determine if theres a winner yet, and sends back the board state data. this cycle repeats until the boardstate is evaluated to be either a win or a draw.

# how to use it

using [localtunnel](https://theboroer.github.io/localtunnel-www/) `npm install localtunnel`

<!-- prettier-ignore -->
1. `git clone` the main branch of the repo
69. Download the required Python libraries (Should be built-in to Python 3+)
420. `cd` to the `server/` folder
4123. run `npm install` to install dependencies for the server (assuming node.js and npm is installed)
321. run `npm run start`, and you should see a message that says `Listening on *:{port}`.
1236. in another terminal, run `lt -p {port} -s {name}` with port being the port that was given in step 5. name of the server is optional, but recommended
73231. `cd` to the `game/` folder, and run `python tictactoe.py` (both people should do this)
358. give the url you got in step 6 to your partner.
349. enjoy
174451230. (because i want it to be 10 steps) have fun

# TODO

- make it work done
- make the server done
- redo the python part ddone

- play again popup after game end (gameplay loop)
- usernames and display of usernames
- display scores

(server)

- implement web sockets to make it FAST
