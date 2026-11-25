// 안전한 SQL — 탐지되면 안 된다
const mysql = require("mysql2");
const express = require("express");
const pool = mysql.createPool({ host: "db" });
const app = express();
const SORTS = ["name", "created_at"];

app.get("/users", (req, res) => {
  // ok: mois-1-01-sql-injection-js 자리표시자와 값 배열
  pool.query("SELECT * FROM users WHERE name = ?", [req.query.name], (e, rows) => res.json(rows));
  // ok: mois-1-01-sql-injection-js 자리표시자와 값 배열 (execute)
  pool.execute("SELECT * FROM users WHERE id = ?", [req.params.id]);
  // ok: mois-1-01-sql-injection-js 객체 형태 — 문장은 고정, 입력은 values
  pool.query({ sql: "SELECT * FROM t WHERE c = ?", values: [req.body.c] });
  // ok: mois-1-01-sql-injection-js 드라이버의 escape 로 값 리터럴을 만든다
  pool.query("SELECT * FROM users WHERE name = " + mysql.escape(req.query.name));
  // ok: mois-1-01-sql-injection-js 숫자로 변환
  pool.query("SELECT * FROM users LIMIT " + parseInt(req.query.limit, 10));
});

app.get("/sorted", (req, res) => {
  const sort = req.query.sort;
  if (!SORTS.includes(sort)) {
    return res.status(400).json({ error: "bad sort" });
  }
  // ok: mois-1-01-sql-injection-js 허용 목록 검사에 실패하면 빠져나간다
  pool.query("SELECT * FROM users ORDER BY " + sort);
  res.end();
});
