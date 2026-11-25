// 안전한 파일 접근 — 탐지되면 안 된다
const fs = require("fs");
const path = require("path");
const express = require("express");
const app = express();
const BASE = path.resolve(__dirname, "uploads");

app.get("/file", (req, res) => {
  // ok: mois-1-03-path-traversal-js 파일 이름만 남긴 값
  fs.createReadStream(path.join(BASE, path.basename(req.query.name))).pipe(res);
});

app.get("/file2", (req, res) => {
  const p = path.resolve(BASE, req.query.name);
  if (!p.startsWith(BASE + path.sep)) {
    return res.sendStatus(403);
  }
  // ok: mois-1-03-path-traversal-js 정규화한 경로가 기준 디렉터리 + 구분자로 시작하지 않으면 빠져나간다
  fs.createReadStream(p).pipe(res);
});

app.get("/file3", (req, res) => {
  const p = path.join(BASE, req.query.name);
  if (!p.startsWith(`${BASE}/`)) throw new Error("outside");
  // ok: mois-1-03-path-traversal-js join 으로 정규화하고 구분자를 붙인 접두 비교
  fs.createReadStream(p).pipe(res);
});

app.get("/static/:f", (req, res) => {
  // ok: mois-1-03-path-traversal-js root 옵션을 주면 Express 가 .. 를 막는다
  res.sendFile(req.params.f, { root: BASE });
  // ok: mois-1-03-path-traversal-js 입력은 파일 내용이고 경로는 고정
  fs.writeFileSync(path.join(BASE, "log.txt"), req.query.msg);
});
