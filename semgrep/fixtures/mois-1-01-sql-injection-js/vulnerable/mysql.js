// SQL 삽입 — 외부 입력을 이어 붙인 문장
const mysql = require("mysql2");
const express = require("express");
const pool = mysql.createPool({ host: "db" });
const app = express();
const SORTS = ["name", "created_at"];

app.get("/users", (req, res) => {
  const name = req.query.name;
  // ruleid: mois-1-01-sql-injection-js
  pool.query("SELECT * FROM users WHERE name = '" + name + "'", (e, rows) => res.json(rows));
  // ruleid: mois-1-01-sql-injection-js
  pool.execute(`SELECT * FROM users WHERE id = ${req.params.id}`);
  const sql = "DELETE FROM sessions WHERE token = '" + req.cookies.token + "'";
  // ruleid: mois-1-01-sql-injection-js
  pool.query(sql);
  // ruleid: mois-1-01-sql-injection-js
  pool.query({ sql: "SELECT * FROM t WHERE c = " + req.body.c, values: [] });
});

app.get("/sorted", (req, res) => {
  const sort = req.query.sort;
  if (SORTS.includes(sort) && req.query.strict) {
    // ruleid: mois-1-01-sql-injection-js
    pool.query("SELECT * FROM users ORDER BY " + sort);
  }
  res.end();
});

async function koa(ctx) {
  const { Client } = require("pg");
  const client = new Client();
  // ruleid: mois-1-01-sql-injection-js
  await client.query({ text: `SELECT * FROM items WHERE tag = '${ctx.query.tag}'` });
}
