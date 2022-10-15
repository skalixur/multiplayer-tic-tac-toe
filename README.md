# Multiplayer tic tac toe

Multiplayer tic tac toe collaboration with @[ricsirogi](https://github.com/ricsirogi)

# how itll work (maybe)

## the server (maybe)

clients `POST` game info (location of pick, players, playernames*, and other game info)

clients then `GET` game info, with logic processed by the server (board state, winners, score, possible pick locations, and other info that needs to be transferred from clients)

^ this will work depending on how i make the server

^ a smarter method would probably be using websockets but idk how to use those so i guess i gotta learn ¯\\\_(ツ)_/¯

# how to use it

## the server part

1. `git clone` the repo
2. `cd` to the `server/` folder
3. run `npm i` to install dependencies (assuming node.js and npm installed)
4. run `npm run start`

# TODO

- make it work
- make the server
- redo the python part