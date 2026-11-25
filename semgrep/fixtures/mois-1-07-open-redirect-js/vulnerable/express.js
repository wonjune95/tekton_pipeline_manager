// 신뢰되지 않는 URL 로 자동 이동 — 서버
const express = require("express");
const app = express();
const ALLOWED = ["/home", "/profile"];

app.get("/login/callback", (req, res) => {
  const next = req.query.next;
  // ruleid: mois-1-07-open-redirect-js
  res.redirect(next);
});

app.get("/go", (req, res) => {
  // ruleid: mois-1-07-open-redirect-js
  res.redirect(302, "/" + req.query.path);
});

app.get("/out", (req, res) => {
  // ruleid: mois-1-07-open-redirect-js
  res.location(`https://${req.query.host}/landing`);
  // ruleid: mois-1-07-open-redirect-js
  res.setHeader("Location", "https://partner.example.com" + req.query.p);
  res.status(302).end();
});

app.get("/raw", (req, res) => {
  // ruleid: mois-1-07-open-redirect-js
  res.writeHead(302, { Location: req.get("referer") });
  res.end();
});

app.get("/checked-late", (req, res) => {
  const u = req.query.u;
  if (!ALLOWED.includes(u)) {
    console.log("unexpected redirect", u);
  }
  // ruleid: mois-1-07-open-redirect-js
  res.redirect(u);
});

app.get("/sliced", (req, res) => {
  // ruleid: mois-1-07-open-redirect-js
  res.redirect(`/a/${req.query.u}`.slice(2));
});

async function koa(ctx) {
  // ruleid: mois-1-07-open-redirect-js
  ctx.redirect(ctx.query.returnTo);
}
