// 안전한 형태 — 탐지되면 안 된다
const cp = require("child_process");
const { execFile, spawn } = require("child_process");
const express = require("express");
const app = express();
const ALLOWED = ["status", "uptime"];
const TOOLS = new Set(["git", "node"]);

app.get("/svc", (req, res) => {
  const c = req.query.c;
  if (!ALLOWED.includes(c)) {
    return res.status(400).send("bad");
  }
  // ok: mois-1-05-os-command-injection-js 허용 목록 검사에 실패하면 빠져나간다
  cp.exec("systemctl " + c);
});

app.get("/svc2", (req, res) => {
  const c = req.query.c;
  if (c == null || !TOOLS.has(c)) throw new Error("bad");
  // ok: mois-1-05-os-command-injection-js null 검사와 || 로 묶은 허용 목록 검사
  cp.exec(c + " --version");
});

app.get("/svc3", (req, res) => {
  const c = req.query.c;
  if (ALLOWED.includes(c)) {
    // ok: mois-1-05-os-command-injection-js 허용 목록 검사를 통과한 if 안
    cp.execSync("systemctl " + c);
  }
  res.end();
});

app.get("/user/:name", (req, res) => {
  const name = req.params.name;
  if (!/^[a-z0-9_-]{1,32}$/.test(name)) return res.sendStatus(400);
  // ok: mois-1-05-os-command-injection-js 영문·숫자·_·- 만 허용하는 전체 일치 정규식
  cp.exec("id " + name);
});

app.get("/user2/:name", (req, res) => {
  const name = req.params.name;
  if (/^\w+$/.test(name)) {
    // ok: mois-1-05-os-command-injection-js 전체 일치 정규식을 통과한 if 안
    cp.exec("id " + name);
  }
  if (name === "root") {
    // ok: mois-1-05-os-command-injection-js 리터럴과 === 비교
    cp.exec("id " + name);
  }
  res.end();
});

app.get("/count", (req, res) => {
  const n = parseInt(req.query.n, 10);
  // ok: mois-1-05-os-command-injection-js 숫자로 변환한 값
  cp.exec("head -n " + n + " /var/log/app.log");
  // ok: mois-1-05-os-command-injection-js 숫자로 변환한 값
  cp.exec(`seq ${Number(req.query.m)}`);
});

app.get("/git", (req, res) => {
  const ref = req.query.ref;
  // ok: mois-1-05-os-command-injection-js 실행 파일 고정, 셸 없이 인자 배열로 전달
  execFile("git", ["log", "--oneline", ref], (e, out) => res.send(out));
  // ok: mois-1-05-os-command-injection-js 셸을 명시적으로 끈 spawn
  spawn("grep", ["-r", ref, "/srv/docs"], { shell: false });
  // ok: mois-1-05-os-command-injection-js 정규식의 exec 는 명령 실행이 아니다
  const m = /^v(\d+)$/.exec(ref);
  res.end();
});
