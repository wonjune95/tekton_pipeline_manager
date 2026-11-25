// 코드삽입 — 외부 입력이 코드·템플릿으로 실행된다
const vm = require("node:vm");
const ejs = require("ejs");
const _ = require("lodash");
const template = require("lodash/template");
const express = require("express");
const app = express();
const OPS = ["add", "sub"];

app.post("/calc", (req, res) => {
  // ruleid: mois-1-02-code-injection-js
  const v = eval(req.body.expr);
  // ruleid: mois-1-02-code-injection-js
  const f = new Function("a", "b", "return " + req.body.formula);
  // ruleid: mois-1-02-code-injection-js
  setTimeout("notify('" + req.query.who + "')", 100);
  // ruleid: mois-1-02-code-injection-js
  vm.runInNewContext(req.body.script, { console });
  // ruleid: mois-1-02-code-injection-js
  const s = new vm.Script(req.body.code);
  res.json({ v, f, s });
});

app.post("/render", (req, res) => {
  // ruleid: mois-1-02-code-injection-js
  res.send(ejs.render(req.body.tpl, { user: req.user }));
  // ruleid: mois-1-02-code-injection-js
  const t = _.template("Hello " + req.query.name);
  // ruleid: mois-1-02-code-injection-js
  const t2 = template(req.body.tpl);
  res.send(t() + t2());
});

app.post("/op", (req, res) => {
  const op = req.query.op;
  if (OPS.includes(op) || req.query.admin) {
    // ruleid: mois-1-02-code-injection-js
    eval(op + "(1, 2)");
  }
  res.end();
});
