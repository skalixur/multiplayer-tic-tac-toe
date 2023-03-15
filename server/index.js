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
  player2Score = 0

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
  })

  socket.on('disconnect', reason => {
    console.table({
      INFO: 'Someone disconnected! Disconnecting all clients.',
      connectionCount: io.engine.clientsCount,
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
      !data?.player_name ||
      (!data?.player && data.player > 0 && data.player < 3)
    )
      return
    if (data.player === 1) player1Name = data.player_name
    else player2Name = data.player_name
    io.emit('playernames', { player1Name, player2Name })
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

    // test for winner
    if (XWinsRegex.test(boardState)) {
      player1Score++
      winner = 'X'
    } else if (OWinsRegex.test(boardState)) {
      player2Score++
      winner = 'O'
    } else if (turnCount === 9) winner = '_'

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
