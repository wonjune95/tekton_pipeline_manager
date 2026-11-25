// 경로 조작 — 외부 입력이 파일 경로에 들어간다
const fs = require("fs");
const fsp = require("fs").promises;
const { unlinkSync, rename: mv } = require("node:fs");
const path = require("path");
const express = require("express");
const app = express();
const BASE = path.resolve(__dirname, "uploads");

app.get("/file", (req, res) => {
  // ruleid: mois-1-03-path-traversal-js
  fs.readFile(path.join(BASE, req.query.name), (e, d) => res.send(d));
  // ruleid: mois-1-03-path-traversal-js
  fs.createReadStream(BASE + "/" + req.query.name).pipe(res);
});

app.delete("/file/:name", async (req, res) => {
  // ruleid: mois-1-03-path-traversal-js
  unlinkSync(`${BASE}/${req.params.name}`);
  // ruleid: mois-1-03-path-traversal-js
  await fsp.writeFile(req.body.target, "x");
  // ruleid: mois-1-03-path-traversal-js
  mv("/tmp/a.txt", path.resolve(BASE, req.body.dest), () => {});
  res.end();
});

app.get("/dl", (req, res) => {
  // ruleid: mois-1-03-path-traversal-js
  res.download(path.join(__dirname, "files", req.query.f));
  // ruleid: mois-1-03-path-traversal-js
  res.sendFile(req.params[0]);
});

app.get("/weak-check", (req, res) => {
  const p = path.resolve(BASE, req.query.name);
  if (!p.startsWith(BASE)) return res.sendStatus(403); // 구분자 없는 접두 비교
  // ruleid: mois-1-03-path-traversal-js
  fs.readFile(p, (e, d) => res.send(d));
});

app.get("/check-continues", (req, res) => {
  const p = path.resolve(BASE, req.query.name);
  if (!p.startsWith(BASE + path.sep)) {
    console.warn("outside", p); // 실패해도 계속 진행
  }
  // ruleid: mois-1-03-path-traversal-js
  fs.readFile(p, (e, d) => res.send(d));
});

app.get("/check-other-base", (req, res) => {
  const p = path.resolve(BASE, req.query.name);
  if (!p.startsWith("/" + path.sep)) return res.sendStatus(403); // 다른 기준
  // ruleid: mois-1-03-path-traversal-js
  fs.readFile(p, (e, d) => res.send(d));
});

app.get("/check-not-resolved", (req, res) => {
  const p = BASE + "/" + req.query.name; // 정규화하지 않은 경로 (.. 가 남는다)
  if (!p.startsWith(BASE + path.sep)) return res.sendStatus(403);
  // ruleid: mois-1-03-path-traversal-js
  fs.readFile(p, (e, d) => res.send(d));
});
