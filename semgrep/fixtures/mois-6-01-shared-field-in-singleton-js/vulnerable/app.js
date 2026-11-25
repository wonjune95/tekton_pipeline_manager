const express = require('express');
const app = express();

let currentUser = null;
var hits = 0;
let lastQuery;

app.get('/me', (req, res) => {
  // ruleid: mois-6-01-shared-field-in-singleton-js
  currentUser = req.session.user;
  res.json(currentUser);
});

app.get('/count', function (req, res) {
  // ruleid: mois-6-01-shared-field-in-singleton-js
  hits++;
  res.send(String(hits));
});

app.get('/search', async (req, res) => {
  if (req.query.q) {
    // ruleid: mois-6-01-shared-field-in-singleton-js
    lastQuery = req.query.q;
  }
  res.json(await search(lastQuery));
});

function makeRouter() {
  const router = express.Router();
  let token = '';
  router.post('/login', (req, res) => {
    // ruleid: mois-6-01-shared-field-in-singleton-js
    token = req.body.token;
    res.end();
  });
  return router;
}
