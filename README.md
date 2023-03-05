# Multiplayer tic tac toe

Multiplayer tic tac toe collaboration with @[ricsirogi](https://github.com/ricsirogi)

# how itll work (maybe)

## the server (maybe)

clients `POST` game info (location of pick, players, playernames\*, and other game info)

clients then `GET` game info, with logic processed by the server (board state, winners, score, possible pick locations, and other info that needs to be transferred from clients)

^ this will work depending on how i make the server

^ a smarter method would probably be using websockets but idk how to use those so i guess i gotta learn ¯\\\_(ツ)\_/¯(but he wont :) )

# how to use it

(using localtunnel https://theboroer.github.io/localtunnel-www/)

1. download the main branch
2. download the python libraries tictactoe.py uses using pip
3. open multiplayer-tic-tac-toe\server in cmd
4. type "node ." (without ") -> Now the server is running
5. type lt -p [the port you want to use (4 digits)] -s [name of the server, optional, but recommended]
6. send the url that you get from this to your partner and they can use it to connect
7. enjoy

## the server part

1. `git clone` the repo
2. `cd` to the `server/` folder
3. run `npm i` to install dependencies (assuming node.js and npm installed)
4. run `npm run start`
5. also port forward :)

# TODO

- make it work done
- make the server done
- redo the python part ddone

- play again popup after game end (gameplay loop)
- usernames and display of usernames
- display scores
