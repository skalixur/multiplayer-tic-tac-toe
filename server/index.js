const express = require('express')
const app = express()
const port = process.env.PORT || 2199

let boardState = 'bs:_________',
  isFirstPlayer = true,
  goesFirst = Math.random() >= 0.5,
  turnCount = 0

app.get('/', (req, res, next) => {
  res.status(200).send('the server is still running')
  console.log('/ -> the server is still running')
})

app.post('/clear', (req, res, next) => {
  boardState = 'bs:_________'
  turnCount = 0
  isFirstPlayer = true
  goesFirst = Math.random() >= 0.5
  res.status(200).json({ statusCode: 200, message: 'Everything cleared!' })
  console.log('/clear -> Everything was cleared')
})

app.get('/isfirstplayer', (req, res, next) => {
  if (isFirstPlayer) {
    console.log({ statusCode: 200, goesFirst })
    res.status(200).json({ statusCode: 200, goesFirst })
  }
  if (!isFirstPlayer) {
    console.log({ statusCode: 200, goesFirst: !goesFirst })
    res.status(200).json({ statusCode: 200, goesFirst: !goesFirst })
  }
  if (isFirstPlayer) {
    console.log('isFirstPlayer = false')
    isFirstPlayer = false
  }
})

app.get('/boardstate', (req, res, next) => {
  res.status(200).json({ statusCode: 200, boardState, turnCount })
  console.log(
    'Retruned boardstate: ' + { statusCode: 200, boardState, turnCount }
  )
})

app.post('/boardstate', (req, res, next) => {
  if (!/bs:[_XO]{9}/g.test(req.query.boardstate))
    return res
      .status(400)
      .json({ statusCode: 400, reason: 'Invalid board state' })
  boardState = req.query.boardstate
  turnCount += 1 /////////////////
  res.status(200).json({
    statusCode: 200,
    boardState,
    turnCount,
    message: 'Board state set',
  })
  console.log('Boardstate was posted: ' + boardState)
})

app.listen(port, () => console.log(`Listening on *:${port}`))
