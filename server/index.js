const { Server } = require('socket.io')
const port = process.env.PORT || 2199
let boardState = 'bs:_________',
  isFirstPlayer = true,
  goesFirst = Math.random() >= 0.5,
  turnCount = 0,
  winner = null,
  player1 = { name: '', score: 0, symbol: '' },
  player2 = { name: '', score: 0, symbol: '' }

let XWinsRegex =
  /(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})/g
let OWinsRegex =
  /(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})/g

const io = new Server()

// io.emit('event', data) -> send to ALL clients
// socket.broadcast.emit('event', data) -> send to ALL clients except sender
// io.engine.clientsCount -> Number of clients
// socket.once('one-time-event') -> Receive an event, but once

io.on('connect', (socket) => {
  console.table({
    INFO: 'Someone connected!',
    connectionCount: io.engine.clientsCount,
    connectionId: socket.id,
  })

  socket.on('disconnect', (reason) => {
    console.table({
      INFO: 'Someone disconnected! Disconnecting all clients.',
      connectionCount: io.engine.clientsCount,
      connectionId: socket.id,
      reason,
    })
    io.emit('disconn')
    io.disconnectSockets(true)
    boardState = '_________'
    turnCount = 0
    isFirstPlayer = true
    goesFirst = Math.random() >= 0.5
    winner = null
    player1 = { name: '', score: 0, symbol: '' }
    player2 = { name: '', score: 0, symbol: '' }
  }) // Special -> Occurs on disconnect

  // handle who goes first
  if (isFirstPlayer) {
    isFirstPlayer = false
    socket.emit('goes-first', goesFirst)
  } else {
    socket.emit('goes-first', !goesFirst)
  }

  socket.on('setplayers', (data) => {
    if (
      !data?.playerName ||
      (!data?.player && data.player > 0 && data.player < 3)
    )
      return
    console.table({ INFO: 'Setplayers was triggered', ...data })

    if (data.player === 1) {
      player1.name = data.playerName
      player1.symbol = data.playerSymbol
    } else if (data.player === 2) {
      player2.name = data.playerName
      player2.symbol = data.playerSymbol
    }
    io.emit('players', {
      player1,
      player2,
    })
  })

  socket.on('clear', (data) => {
    if (data?.clearScore === undefined) return
    boardState = '_________'
    turnCount = 0
    isFirstPlayer = true
    goesFirst = Math.random() >= 0.5
    winner = null
    player1.score = data.clearScore ? 0 : player1.score
    player2.score = data.clearScore ? 0 : player2.score
    io.emit(
      'board-state',
      JSON.stringify({
        boardState,
        turnCount,
        winner,
        clear: true,
        player1,
        player2,
      }),
    )

    if (isFirstPlayer) {
      isFirstPlayer = false
      socket.emit('goes-first', goesFirst)
      socket.broadcast.emit('goes-first', !goesFirst)
    }

    console.table({ INFO: 'Everything was cleared', goesFirst })
  })

  socket.on('board-state', (data) => {
    if (/[_XO]{9}/g.test(data.boardstate)) return
    boardState = data
    turnCount += 1
    if (XWinsRegex.test(boardState)) {
      winner = 'X'
    } else if (OWinsRegex.test(boardState)) {
      winner = 'O'
    } else if (turnCount === 9) winner = '_'
    if (winner != '_' && winner != null) {
      if (player1.symbol === winner) player1.score++
      else if (player2.symbol === winner) player2.score++
    }
    console.log(player1, player2)
    io.emit(
      'board-state',
      JSON.stringify({
        boardState,
        turnCount,
        winner,
        clear: false,
        player1,
        player2,
      }),
    )
    console.table({
      INFO: 'Emitted to all:',
      boardState,
      turnCount,
      winner,
      clear: false,
      player1,
      player2,
    })
  })

  socket.on('message', (data) => {
    socket.broadcast.emit(data)
  })

  socket.on('debug', (data) => {
    console.log(data)
    socket.emit('debug', `server response: ${data}`)
  })
})

io.listen(port)

console.log(`Listening on port *:${port}`)
