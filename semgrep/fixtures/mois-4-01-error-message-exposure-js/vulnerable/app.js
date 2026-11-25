const express = require('express');
const errorhandler = require('errorhandler');
const app = express();

app.get('/user/:id', async (req, res) => {
  try {
    res.json(await findUser(req.params.id));
  } catch (e) {
    // ruleid: mois-4-01-error-message-exposure-js
    res.status(500).send(e.stack);
  }
});

app.get('/order/:id', (req, res) => {
  findOrder(req.params.id)
    .then((o) => res.json(o))
    // ruleid: mois-4-01-error-message-exposure-js
    .catch((err) => res.status(500).json({ error: err.message }));
});

app.get('/legacy', function (req, res) {
  db.query('SELECT 1', function (err, rows) {
    if (err) {
      // ruleid: mois-4-01-error-message-exposure-js
      return res.send(err);
    }
    res.json(rows);
  });
});

app.get('/view', (req, res) => {
  try {
    render();
  } catch (error) {
    // ruleid: mois-4-01-error-message-exposure-js
    res.render('error', { error });
  } finally {
    done();
  }
});

// ruleid: mois-4-01-error-message-exposure-js
app.use(errorhandler());

app.use(function (err, req, res, next) {
  // ruleid: mois-4-01-error-message-exposure-js
  res.status(err.status || 500).end(err.toString());
});

function debugPath() {
  // ruleid: mois-4-01-error-message-exposure-js
  console.trace('here');
}

app.post('/save', (req, res) => {
  new Item(req.body).save(function (error) {
    // ruleid: mois-4-01-error-message-exposure-js
    if (error) return res.status(400).json(error);
    res.sendStatus(201);
  });
});
