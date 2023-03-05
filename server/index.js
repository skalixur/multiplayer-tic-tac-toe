const express = require('express')
const app = express()
const port = process.env.PORT || 2199

let boardState = 'bs:_________',
  isFirstPlayer = true,
  goesFirst = Math.random() >= 0.5,
  turnCount = 0,
  winner = null

let XWinsRegex =
  /bs:(XXX[XO_]{6})|([XO_]{3}XXX[XO_]{3})|([XO_]{6}XXX)|(X[XO_]{2}X[XO_]{2}X[XO_]{2})|([XO_]X[XO_]{2}X[XO_]{2}X[XO_])|([XO_]{2}X[XO_]{2}X[XO_]{2}X)|(X[XO_]{3}X[XO_]{3}X)|([XO_]{2}X[XO_]X[XO_]X[XO_]{2})/g
let OWinsRegex =
  /bs:(OOO[XO_]{6})|([XO_]{3}OOO[XO_]{3})|([XO_]{6}OOO)|(O[XO_]{2}O[XO_]{2}O[XO_]{2})|([XO_]O[XO_]{2}O[XO_]{2}O[XO_])|([XO_]{2}O[XO_]{2}O[XO_]{2}O)|(O[XO_]{3}O[XO_]{3}O)|([XO_]{2}O[XO_]O[XO_]O[XO_]{2})/g

app.get('/', (req, res, next) => {
  res.status(200).send('the server is still running')
})

app.post('/clear', (req, res, next) => {
  boardState = 'bs:_________'
  turnCount = 0
  isFirstPlayer = true
  goesFirst = Math.random() >= 0.5
  winner = null
  res.status(200).json({ statusCode: 200, message: 'Everything cleared!' })
})

app.get('/isfirstplayer', (req, res, next) => {
  if (isFirstPlayer) res.status(200).json({ statusCode: 200, goesFirst })

  if (!isFirstPlayer)
    res.status(200).json({ statusCode: 200, goesFirst: !goesFirst })

  if (isFirstPlayer) isFirstPlayer = false
})

app.get('/boardstate', (req, res, next) => {
  res.status(200).json({ statusCode: 200, boardState, turnCount, winner })
})

app.post('/boardstate', (req, res, next) => {
  if (!/bs:[_XO]{9}/g.test(req.query.boardstate))
    return res
      .status(400)
      .json({ statusCode: 400, reason: 'Invalid board state' })
  boardState = req.query.boardstate
  turnCount += 1 /////////////////

  // Determine if there's a winner, and which symbol

  if (XWinsRegex.test(boardState)) winner = 'X'
  else if (OWinsRegex.test(boardState)) winner = 'O'
  else winner = '_'

  res.status(200).json({
    statusCode: 200,
    boardState,
    turnCount,
    winner,
    message: 'Board state set',
  })
})

app.listen(port, () => console.log(`Listening on *:${port}`))
