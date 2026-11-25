const express = require('express');
const app = express();

let started = Date.now();
const cache = new Map();
let hits = 0;

app.get('/me', (req, res) => {
  // ok: mois-6-01-shared-field-in-singleton-js 지역 변수
  let currentUser = req.session.user;
  currentUser = normalize(currentUser);
  res.json(currentUser);
});

app.get('/uptime', (req, res) => {
  // ok: mois-6-01-shared-field-in-singleton-js 읽기만 한다
  res.json({ uptime: Date.now() - started });
});

function reset() {
  // ok: mois-6-01-shared-field-in-singleton-js 요청 처리 함수가 아니다
  started = Date.now();
}

let total = 0;
app.get('/sum', (req, res) => {
  var total = 0;
  for (const n of req.query.n) {
    // ok: mois-6-01-shared-field-in-singleton-js var 로 다시 선언한 지역 변수
    total += Number(n);
  }
  res.json({ total });
});

app.post('/chat', async (req, res) => {
  const tools = {
    search: async ({ query }) => {
      // ok: mois-6-01-shared-field-in-singleton-js 안쪽 함수의 지역 선언
      const products = await find(query);
      return products;
    },
  };
  if (req.body.reset) {
    let hits = 0;
    // ok: mois-6-01-shared-field-in-singleton-js 안쪽 블록의 지역 변수
    hits++;
    res.json({ hits });
  }
  res.json(await run(tools));
});
