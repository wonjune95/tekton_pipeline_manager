// 서버 응답 본문에 외부 입력을 그대로 출력하는 예
const express = require('express');
const escapeHtml = require('escape-html');
const he = require('he');
const app = express();

app.get('/hello', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.send('<h1>안녕하세요 ' + req.query.name + '</h1>');
});

app.get('/status', (req, res) => {
  const msg = req.query.msg;
  // ruleid: mois-1-04-xss-js
  res.status(400).send(`<p>${msg}</p>`);
});

app.get('/raw', function (req, res) {
  // ruleid: mois-1-04-xss-js
  res.write(req.params.id);
  // ruleid: mois-1-04-xss-js
  res.end(req.get('X-Name'));
});

// JSON 문자열도 Content-Type 을 정하지 않으면 text/html 로 나간다
app.post('/echo', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.send(JSON.stringify({ name: req.body.name }));
});

// 형식을 HTML 로 정한 응답
app.get('/html', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.type('html').send(req.query.q);
});

// 속이는 예: 이스케이프했지만 href 안 (javascript: URL 을 막지 못함)
app.get('/link', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.send("<a href='" + escapeHtml(req.query.url) + "'>이동</a>");
});

// 속이는 예: 템플릿의 속성 자리
app.get('/attr', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.send(`<img src="${he.encode(req.query.img)}">`);
});

// 속이는 예: 이스케이프 결과를 변수에 받았다가 이벤트 핸들러 안에 넣음
app.get('/onclick', (req, res) => {
  const v = escapeHtml(req.query.v);
  // ruleid: mois-1-04-xss-js
  res.send('<button onclick="go(\'' + v + '\')">go</button>');
});

app.get('/tplvar', (req, res) => {
  const v = he.encode(req.query.v);
  // ruleid: mois-1-04-xss-js
  res.send(`<a title=${v}>x</a>`);
});

// 속이는 예: 닫히지 않은 <script 안
app.get('/script', (req, res) => {
  // ruleid: mois-1-04-xss-js
  res.send('<script>var q = "' + escapeHtml(req.query.q) + '";</script>');
});

// 속이는 예: 형식을 정했지만 HTML
app.get('/typed', (req, res) => {
  res.set('Content-Type', 'text/html');
  // ruleid: mois-1-04-xss-js
  res.send(req.query.q);
});

// 속이는 예: 형식 지정이 다른 응답 객체
app.get('/other', (req, res) => {
  other.type('text/plain');
  // ruleid: mois-1-04-xss-js
  res.send(req.query.q);
});
