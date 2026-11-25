// 안전한 서버 측 요청 — 탐지되면 안 된다
const axios = require("axios");
const http = require("http");
const express = require("express");
const app = express();
const HOSTS = ["api.example.com", "cdn.example.com"];

app.get("/user/:id", async (req, res) => {
  // ok: mois-1-12-ssrf-js 스킴·호스트가 고정되고 입력은 경로 자리
  const u = await axios.get("https://api.example.com/users/" + req.params.id);
  // ok: mois-1-12-ssrf-js 스킴·호스트가 고정된 템플릿 리터럴
  const r = await fetch(`https://api.example.com/search?q=${encodeURIComponent(req.query.q)}`);
  // ok: mois-1-12-ssrf-js 호스트가 고정되고 입력은 path 항목
  http.request({ host: "internal.example.com", path: "/items/" + req.query.item });
  // ok: mois-1-12-ssrf-js 주소는 고정, 입력은 본문
  await axios.post("https://hooks.example.com/notify", { text: req.body.text });
  res.json(u.data);
});

app.get("/mirror", async (req, res) => {
  const host = req.query.host;
  if (!HOSTS.includes(host)) {
    return res.status(400).end();
  }
  // ok: mois-1-12-ssrf-js 허용 목록 검사에 실패하면 빠져나간다
  const r = await fetch("https://" + host + "/data.json");
  res.json(await r.json());
});
