const express = require('express');
const router = express.Router();

router.post('/login', async (req, res) => {
  // ruleid: mois-6-02-debug-code-js
  console.log('login', req.body);
  // ruleid: mois-6-02-debug-code-js
  debugger;
  const user = await auth(req.body.id, req.body.password);
  // ruleid: mois-6-02-debug-code-js
  console.dir(user, { depth: null });
  res.json(user);
});
