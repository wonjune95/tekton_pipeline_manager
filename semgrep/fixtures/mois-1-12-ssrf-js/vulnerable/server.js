// 서버사이드 요청 위조 — 외부 입력이 요청 주소에 들어간다
const axios = require("axios");
const http = require("http");
const got = require("got");
const { get: httpsGet } = require("https");
const express = require("express");
const app = express();
const HOSTS = ["api.example.com"];

app.get("/preview", async (req, res) => {
  const url = req.query.url;
  // ruleid: mois-1-12-ssrf-js
  const r = await fetch(url);
  // ruleid: mois-1-12-ssrf-js
  const a = await axios.get(url);
  // ruleid: mois-1-12-ssrf-js
  await axios({ method: "get", url: req.body.target });
  // ruleid: mois-1-12-ssrf-js
  http.get(`http://${req.query.host}:8080/health`);
  // ruleid: mois-1-12-ssrf-js
  http.request({ host: req.query.host, path: "/" });
  // ruleid: mois-1-12-ssrf-js
  await got("https://api.example.com" + req.query.path);
  // ruleid: mois-1-12-ssrf-js
  httpsGet(req.headers["x-callback"]);
  res.send(await r.text());
});

app.get("/proxy", async (req, res) => {
  const host = req.query.host;
  if (!HOSTS.includes(host)) {
    res.status(400); // 실패해도 계속 진행
  }
  // ruleid: mois-1-12-ssrf-js
  const r = await fetch("https://" + host + "/data");
  res.send(await r.text());
});
