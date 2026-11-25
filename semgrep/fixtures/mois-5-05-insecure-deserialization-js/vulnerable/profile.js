const express = require('express');
const serialize = require('node-serialize');
const yaml = require('js-yaml');
const funcster = require('funcster');
const router = express.Router();

router.get('/profile', (req, res) => {
  const raw = Buffer.from(req.cookies.profile, 'base64').toString();
  // ruleid: mois-5-05-insecure-deserialization-js
  const profile = serialize.unserialize(raw);
  res.json(profile);
});

router.post('/import', (req, res) => {
  // ruleid: mois-5-05-insecure-deserialization-js
  const doc = yaml.load(req.body.yaml, { schema: yaml.DEFAULT_FULL_SCHEMA });
  res.json(doc);
});

router.post('/fn', (req, res) => {
  // ruleid: mois-5-05-insecure-deserialization-js
  const fn = funcster.deepDeserialize(req.body.fn);
  res.json(fn);
});
