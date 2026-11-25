const express = require('express');
const errorhandler = require('errorhandler');
const logger = require('./logger');
const app = express();

app.get('/user/:id', async (req, res) => {
  try {
    res.json(await findUser(req.params.id));
  } catch (e) {
    logger.error(e);
    // ok: mois-4-01-error-message-exposure-js 정해진 문구만 응답
    res.status(500).send('internal error');
  }
});

app.get('/legacy', function (req, res) {
  db.query('SELECT 1', function (err, rows) {
    if (err) {
      logger.error(err);
      // ok: mois-4-01-error-message-exposure-js 정해진 문구만 응답
      return res.sendStatus(500);
    }
    // ok: mois-4-01-error-message-exposure-js 결과 행은 오류가 아니다
    res.json(rows);
  });
});

if (process.env.NODE_ENV === 'development') {
  // ok: mois-4-01-error-message-exposure-js 개발 환경에서만 켠다
  app.use(errorhandler());
}

app.use(function (err, req, res, next) {
  logger.error(err);
  // ok: mois-4-01-error-message-exposure-js 상태 코드와 고정 문구
  res.status(500).json({ error: 'internal error' });
});

app.get('/me', (req, res) => {
  findUser(req.user.id).then((user) => {
    // ok: mois-4-01-error-message-exposure-js 조회 결과(오류 아님)
    if (user) res.json(user);
  });
});
