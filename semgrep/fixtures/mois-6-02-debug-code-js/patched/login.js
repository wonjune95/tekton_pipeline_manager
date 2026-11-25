const express = require('express');
const logger = require('./logger');
const router = express.Router();

router.post('/login', async (req, res) => {
  const user = await auth(req.body.id, req.body.password);
  // ok: mois-6-02-debug-code-js 로거
  logger.info('login', { id: req.body.id });
  res.json(user);
});

router.use((err, req, res, next) => {
  // ok: mois-6-02-debug-code-js 오류 기록
  console.error(err);
  res.sendStatus(500);
});

if (require.main === module) {
  // ok: mois-6-02-debug-code-js 명령행 실행 블록
  console.log('usage: node login.js');
}
