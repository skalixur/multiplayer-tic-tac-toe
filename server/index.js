const { Server } = require('socket.io')
const port = process.env.PORT || 2199
let boardState = 'bs:_________',
  isFirstPlayer = true,
  goesFirst = Math.random() >= 0.5,
  turnCount = 0,
  winner = null

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
  console.log(`Someone connected!\nConnection count: ${io.engine.clientsCount}`)

  // handle who goes first
  if (isFirstPlayer) {
    isFirstPlayer = false
    socket.emit('goes-first', goesFirst)
  } else socket.emit('goes-first', !goesFirst)

  socket.on('clear', data => {
    boardState = '_________'
    turnCount = 0
    isFirstPlayer = true
    goesFirst = Math.random() >= 0.5
    winner = null
    socket.emit('debug-events', 'Everything cleared!')
    io.emit(
      'board-state',
      JSON.stringify({ boardState, turnCount, winner, clear: true })
    )
    console.log('Everything was cleared')
  })

  socket.on('board-state', data => {
    if (/[_XO]{9}/g.test(data.boardstate)) return
    boardState = data
    turnCount += 1

    // test for winner
    if (XWinsRegex.test(boardState)) winner = 'X'
    else if (OWinsRegex.test(boardState)) winner = 'O'
    else if (turnCount === 9) winner = '_'

    io.emit('board-state', JSON.stringify({ boardState, turnCount, winner }))
    console.log(`Received: ${data}`)
    console.log(`Emitted to all:`)
    console.log({ boardState, turnCount, winner, clear: false })
  })

  socket.on('debug', data => {
    console.log(data)
    socket.emit('debug', 'debuggg')
  })

  socket.on('disconnect', reason => {
    console.log(
      `Someone disconnected!\nConnection count: ${io.engine.clientsCount}\nReason: ${reason}`
    )
  }) // Special -> Occurs on disconnect
})

io.listen(port)

console.log(`Listening on port *:${port}`)
