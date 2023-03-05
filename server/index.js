const express = require('express')
const app = express()
const port = process.env.PORT || 2199

let player1 // | \/
let player2 // | example player variables
let boardState = 'bs:_________'
let isFirstPlayer = true
let turnCount = 0

// 0 > 1st player 1st turn - 0 -> 1
// 1 -> 2nd player 1st turn - 1 -> 2

app.get('/turncount', (req, res, next) => {
  res.status(200).json({ statusCode: 200, turnCount })
})

app.post('/clear', (req, res, next) => {
  boardState = 'bs:_________'
  turnCount = 0
  isFirstPlayer = true
  res.status(200).json({ statusCode: 200, message: 'Everything cleared!' })
})

app.get('/isfirstplayer', (req, res, next) => {
  res.status(200).json({ statusCode: 200, isFirstPlayer })
  if (isFirstPlayer) isFirstPlayer = false
})

app.get('/', (req, res, next) => {
  res.status(200).send('the server is still running')
})

app.get('/boardstate', (req, res, next) => {
  res.status(200).json({ statusCode: 200, boardState })
})

app.post('/boardstate', (req, res, next) => {
  if (!/bs:[_XO]{9}/g.test(req.query.boardstate))
    return res
      .status(400)
      .json({ statusCode: 400, reason: 'Invalid board state' })
  boardState = req.query.boardstate
  turnCount += 1
  res
    .status(200)
    .json({ statusCode: 200, boardState, message: 'Board state set' })
  console.log(boardState)
})

app.post('/players/players', (req, res, next) => {
  console.log(req.query)
  if (!req.query.player1 || !req.query.player2)
    return res.status(400).json({ statusCode: 400, reason: 'Invalid request' })

  player1 = req.query.player1
  player2 = req.query.player2
  res.status(200).json({
    statusCode: 200,
    player1: req.query.player1,
    player2: req.query.player2,
  })
})

app.get('/players', (req, res, next) => {
  // when GET requesting players, return current player variables
  if (!player1 || !player2)
    return res.status(404).json({
      statusCode: 404,
      reason: 'Player 1 or Player 2 has not yet been set.',
    })
  res.status(200).json({ statusCode: 200, player1, player2 })
})

app.listen(port, () => console.log(`Listening on *:${port}`))
