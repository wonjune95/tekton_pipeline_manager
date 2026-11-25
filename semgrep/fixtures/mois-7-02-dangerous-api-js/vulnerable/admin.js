const express = require('express');
const router = express.Router();

router.post('/shutdown', (req, res) => {
  res.send('bye');
  // ruleid: mois-7-02-dangerous-api-js
  process.exit(0);
});

router.get('/item/:id', async function (req, res) {
  const item = await find(req.params.id);
  if (!item) {
    // ruleid: mois-7-02-dangerous-api-js
    process.abort();
  }
  res.json(item);
});

function encode(s) {
  // ruleid: mois-7-02-dangerous-api-js
  return new Buffer(s).toString('base64');
}

function legacy(n) {
  // ruleid: mois-7-02-dangerous-api-js
  return Buffer(n);
}

router.get('/pad', (req, res) => {
  // ruleid: mois-7-02-dangerous-api-js
  const buf = Buffer.allocUnsafe(Number(req.query.size));
  res.send(buf);
});

router.get('/pad2', (req, res) => {
  const size = parseInt(req.query.size, 10);
  // ruleid: mois-7-02-dangerous-api-js
  const buf = Buffer.allocUnsafeSlow(size);
  res.send(buf);
});
