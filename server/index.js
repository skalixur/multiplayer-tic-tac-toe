const { Server } = require('socket.io')
const port = process.env.PORT || 2199
let boardState = 'bs:_________',
  isFirstPlayer = true,
  goesFirst = Math.random() >= 0.5,
  turnCount = 0,
  winner = null,
  player1Name = '',
  player2Name = '',
  player1Score = 0,
  player2Score = 0,
  playerDict = {}
  set = false

let XWinsRegex =
  /(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})/g
let OWinsRegex =
  /(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})/g

const io = new Server()

// io.emit('event', data) -> send to ALL clients
// socket.broadcast.emit('event', data) -> send to ALL clients except sender
// io.engine.clientsCount -> Number of clients
// socket.once('one-time-event') -> Receive an event, but once

io.on('connect', socket => {
  console.table({
    INFO: 'Someone connected!',
    connectionCount: io.engine.clientsCount,
    connectionId: socket.id,
  })

  socket.on('disconnect', reason => {
    console.table({
      INFO: 'Someone disconnected! Disconnecting all clients.',
      connectionCount: io.engine.clientsCount,
      connectionId: socket.id,
      reason,
    })
    io.disconnectSockets(true)
    boardState = '_________'
    turnCount = 0
    isFirstPlayer = true
    goesFirst = Math.random() >= 0.5
    winner = null
    player1Score = 0
    player2Score = 0
    player1Name = ''
    player2Name = ''
    playerDict = {}
    set = false
  }) // Special -> Occurs on disconnect

  // handle who goes first
  if (isFirstPlayer) {
    isFirstPlayer = false
    socket.emit('goes-first', goesFirst)
  } else {
    socket.emit('goes-first', !goesFirst)
  }

  socket.on('setplayers', data => {
    if (
      !data?.playerName ||
      (!data?.player && data.player > 0 && data.player < 3)
    )
      return
    console.table({ INFO: 'Setplayers was triggered', ...data })
    if (data.player === 1) player1Name = data.playerName
    else player2Name = data.playerName
    io.emit('playernames', { player1Name, player2Name })

    // set the ACTUAL first and second player which will be permanent
    // now I know the name and symbol of each player
    if (set === false) {
      playerDict = {player1: [player1Name, player1Score],
                  player2: [player2Name, player2Score]}
      if (playerDict["player1"][0] != "" && playerDict["player2"][0] != ""){ // when we have both players' names, lock them in
        set = true
      }}
  })

  socket.on('clear', data => {
    if (data?.clearScore === undefined) return
    boardState = '_________'
    turnCount = 0
    isFirstPlayer = true
    goesFirst = Math.random() >= 0.5
    winner = null
    player1Score = data.clearScore ? 0 : player1Score
    player2Score = data.clearScore ? 0 : player2Score
    io.emit(
      'board-state',
      JSON.stringify({
        boardState,
        turnCount,
        winner,
        clear: true,
        player1Score,
        player2Score,
        player1Name,
        player2Name,
      })
    )

    if (isFirstPlayer) {
      isFirstPlayer = false
      socket.emit('goes-first', goesFirst)
      socket.broadcast.emit('goes-first', !goesFirst)
    }

    console.table({ INFO: 'Everything was cleared', goesFirst })
  })

  socket.on('board-state', data => {
    if (/[_XO]{9}/g.test(data.boardstate)) return
    boardState = data
    turnCount += 1

    /* test for winner 
    this used to assume that player1 is only x and player 2 is always O
    Now the usernames have a :{symbol} at the end,
    and also theres a dictionary that stores p1 and p2 and their scores
    (the code may be able to be optimized but I don't do js so idk)*/
    if (XWinsRegex.test(boardState)) {
      winner = 'X'
    } else if (OWinsRegex.test(boardState)) {
      winner = 'O'
    } else if (turnCount === 9) winner = '_'
    if (winner != '_') {
      console.log(playerDict)
      if (player1Name.slice(-1) === winner) {
          if (player1Name.slice(0, -1) === playerDict["player1"][0].slice(0, -1)) { // if the current p1 is the actual p1
            playerDict["player1"][1]++ // then the actual p1 gets the point
          } else {
            playerDict["player2"][1]++ // else the actual p2 gets the point
          }
      }
      else if (player2Name.slice(-1) === winner) { 
        if (player2Name.slice(0, -1) === playerDict["player2"][0].slice(0, -1)) { // else if the current p2 is the actual p2 
          playerDict["player2"][1]++ // then the actual p2 gets the point
        } else {
          playerDict["player1"][1]++ // else the actual p1 gets the point
        }
      } 
      try {
        player1Score = playerDict["player1"][1]
        player2Score = playerDict["player2"][1]
      } catch (TypeError) {
        console.log("playerDict[\"player1/2\"][1/2] doesN't exist")
      }
    }

    io.emit(
      'board-state',
      JSON.stringify({
        boardState,
        turnCount,
        winner,
        clear: false,
        player1Score,
        player2Score,
        player1Name,
        player2Name,
      })
    )
    console.table({
      INFO: 'Emitted to all:',
      boardState,
      turnCount,
      winner,
      clear: false,
      player1Score,
      player2Score,
      player1Name,
      player2Name,
    })
  })

  socket.on('message', data => {
    socket.broadcast.emit(data)
  })

  socket.on('debug', data => {
    console.log(data)
    socket.emit('debug', `server response: ${data}`)
  })
})

io.listen(port)

console.log(`Listening on port *:${port}`)
