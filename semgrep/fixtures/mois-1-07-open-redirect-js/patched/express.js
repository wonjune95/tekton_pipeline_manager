// 안전한 이동 — 탐지되면 안 된다
const express = require("express");
const app = express();
const ALLOWED = ["/home", "/profile"];

app.get("/login/callback", (req, res) => {
  const next = req.query.next;
  if (!ALLOWED.includes(next)) {
    return res.redirect("/");
  }
  // ok: mois-1-07-open-redirect-js 허용 목록 검사에 실패하면 빠져나간다
  res.redirect(next);
});

app.get("/article", (req, res) => {
  // ok: mois-1-07-open-redirect-js "/articles/" 로 고정된 상대 경로
  res.redirect("/articles/" + req.query.slug);
  // ok: mois-1-07-open-redirect-js 스킴·호스트가 고정된 주소
  res.location(`https://www.example.com/search?q=${encodeURIComponent(req.query.q)}`);
});

app.get("/page", (req, res) => {
  // ok: mois-1-07-open-redirect-js 숫자로 변환한 값
  res.redirect("/" + parseInt(req.query.page, 10));
  // ok: mois-1-07-open-redirect-js 고정 주소
  res.setHeader("Location", "/home");
  // ok: mois-1-07-open-redirect-js Location 이 아닌 헤더
  res.setHeader("X-Next", req.query.next);
  res.end();
});
