const express = require('express');
const serialize = require('node-serialize');
const yaml = require('js-yaml');
const router = express.Router();

router.get('/profile', (req, res) => {
  const raw = Buffer.from(req.cookies.profile, 'base64').toString();
  // ok: mois-5-05-insecure-deserialization-js JSON.parse 는 함수를 만들지 않는다
  res.json(JSON.parse(raw));
});

router.post('/import', (req, res) => {
  // ok: mois-5-05-insecure-deserialization-js 기본 스키마(js-yaml 4)·안전 스키마
  res.json(yaml.load(req.body.yaml, { schema: yaml.JSON_SCHEMA }));
});

router.post('/export', (req, res) => {
  // ok: mois-5-05-insecure-deserialization-js 직렬화는 위험하지 않다
  res.json({ data: serialize.serialize({ name: req.body.name }) });
});
