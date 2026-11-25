const express = require('express');
const router = express.Router();

router.get('/item/:id', async function (req, res) {
  const item = await find(req.params.id);
  // ok: mois-7-02-dangerous-api-js 오류 응답
  if (!item) return res.sendStatus(404);
  res.json(item);
});

function encode(s) {
  // ok: mois-7-02-dangerous-api-js Buffer.from
  return Buffer.from(s).toString('base64');
}

router.get('/pad', (req, res) => {
  // ok: mois-7-02-dangerous-api-js 0 으로 채운 버퍼
  res.send(Buffer.alloc(Number(req.query.size)));
});

function scratch() {
  // ok: mois-7-02-dangerous-api-js 고정 크기
  return Buffer.allocUnsafe(64);
}

function main() {
  start().catch(() => {
    // ok: mois-7-02-dangerous-api-js 시작 스크립트(요청 처리 함수 아님)
    process.exit(1);
  });
}
