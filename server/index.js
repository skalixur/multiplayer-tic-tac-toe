const express = require('express')
const app = express()
const port = process.env.PORT || 2198

let player1 // | \/
let player2 // | example player variables

app.get('/', (req, res, next) => {
  res.status(200).send('the server is still running')
})

app.post('/boardstate', (req, res, next) => {
  // example post request with board state`
  res.status(200).json(
    JSON.stringify({
      statusCode: 200,
      status: 'OK',
      body: req.body || { msg: 'body was empty' }, // sending back board state
    })
  )
})

app.post('/players', (req, res, next) => {
  if (!req.body.player1 || !req.body.player2)
    return res.status(400).send('bad request')

  player1 = req.body.player1
  player2 = req.body.player2
  res.status(200).send('players set')
})

app.get('/players', (req, res, next) => {
  // when GET requesting players, return current player variables
  if (!player1 || !player2)
    return res.status(404).send('player1 or player2 has not yet been set')
  res.status(200).json(JSON.stringify({ player1, player2 }))
})

app.listen(port, () => console.log(`Listening on *:${port}`))
