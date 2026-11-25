// 안전한 형태 — 탐지되면 안 된다
const ejs = require("ejs");
const express = require("express");
const app = express();
const OPS = ["add", "sub"];
const add = (a, b) => a + b;
const notify = (msg) => add(msg, "");

app.post("/calc", (req, res) => {
  // ok: mois-1-02-code-injection-js 코드 실행이 아니라 JSON 해석
  const data = JSON.parse(req.body.json);
  // ok: mois-1-02-code-injection-js 함수를 넘긴 setTimeout (입력은 데이터로만 쓰인다)
  setTimeout(() => notify(req.query.msg), 10);
  // ok: mois-1-02-code-injection-js 템플릿은 고정, 입력은 데이터
  const html = ejs.render("<p><%= name %></p>", { name: req.query.name });
  // ok: mois-1-02-code-injection-js 템플릿 파일 이름이 고정
  res.render("profile", { name: req.query.name });
  res.json({ html, data });
});

app.post("/op", (req, res) => {
  const op = req.query.op;
  if (!OPS.includes(op)) return res.status(400).end();
  // ok: mois-1-02-code-injection-js 허용 목록 검사에 실패하면 빠져나간다
  const r = eval(op + "(1, 2)");
  // ok: mois-1-02-code-injection-js 숫자로 변환한 값
  const n = eval(String(Number(req.query.n)) + " * 2");
  res.json({ r, n });
});
