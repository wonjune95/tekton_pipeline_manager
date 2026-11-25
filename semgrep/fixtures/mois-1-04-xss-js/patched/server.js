// 안전한 출력
const express = require('express');
const escapeHtml = require('escape-html');
const he = require('he');
const _ = require('lodash');
const sanitizeHtml = require('sanitize-html');
const app = express();

app.get('/hello', (req, res) => {
  // ok: mois-1-04-xss-js 본문 위치에서 이스케이프
  res.send('<h1>안녕하세요 ' + escapeHtml(req.query.name) + '</h1>');
});

app.get('/tpl', (req, res) => {
  // ok: mois-1-04-xss-js 템플릿의 본문 자리
  res.send(`<p>${he.encode(req.query.q)}</p><a href="/list">목록</a>`);
});

app.get('/var', (req, res) => {
  const safe = _.escape(req.query.q);
  // ok: mois-1-04-xss-js 이스케이프 결과를 본문 자리에만 사용
  res.send('<p>' + safe + '</p>');
});

app.get('/json', (req, res) => {
  // ok: mois-1-04-xss-js JSON 응답
  res.json({ q: req.query.q });
  // ok: mois-1-04-xss-js 객체 리터럴은 JSON 으로 응답
  res.send({ q: req.query.q });
});

app.get('/query', (req, res) => {
  // ok: mois-1-04-xss-js 요청 객체 통째(req.query)는 JSON 으로 응답
  res.send(req.query);
});

app.get('/plain', (req, res) => {
  // ok: mois-1-04-xss-js 형식을 text/plain 으로 지정
  res.type('text/plain').send(req.query.q);
});

app.get('/plain2', (req, res) => {
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  // ok: mois-1-04-xss-js 앞 문장에서 형식을 text/plain 으로 지정
  res.end(req.query.q);
});

app.get('/plain3', (req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  // ok: mois-1-04-xss-js writeHead 로 JSON 형식 지정
  res.end(JSON.stringify({ q: req.query.q }));
});

app.get('/num', (req, res) => {
  // ok: mois-1-04-xss-js 숫자로 바꾼 값
  res.send('<p>' + parseInt(req.query.page, 10) + '</p>');
});

app.get('/clean', (req, res) => {
  // ok: mois-1-04-xss-js sanitize-html 기본 설정
  res.send('<div>' + sanitizeHtml(req.body.html) + '</div>');
});

app.get('/misc', (req, res) => {
  // ok: mois-1-04-xss-js URL 인코딩 · 숫자 변환 결과를 본문 자리에 사용
  res.send('<p>' + encodeURIComponent(req.query.a) + ' ' + Number(req.query.b) + ' ' + parseFloat(req.query.c) + '</p>');
});
