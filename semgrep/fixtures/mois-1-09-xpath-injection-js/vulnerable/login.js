// 외부 입력을 XPath 질의문에 이어 붙임
const xpath = require('xpath');
const { DOMParser } = require('@xmldom/xmldom');
const libxmljs = require('libxmljs2');
const fs = require('fs');

const doc = new DOMParser().parseFromString(fs.readFileSync('users.xml', 'utf8'), 'text/xml');

app.post('/login', (req, res) => {
  const { user, pass } = req.body;
  // ruleid: mois-1-09-xpath-injection-js
  const nodes = xpath.select("//user[name='" + user + "' and password='" + pass + "']", doc);
  res.json({ ok: nodes.length > 0 });
});

app.get('/one', (req, res) => {
  // ruleid: mois-1-09-xpath-injection-js
  const n = xpath.select1(`//item[@id='${req.query.id}']`, doc);
  const select = xpath.useNamespaces({ u: 'urn:users' });
  // ruleid: mois-1-09-xpath-injection-js
  const m = select('//u:user[u:name="' + req.query.name + '"]', doc);
  res.json({ n, m });
});

app.get('/lib', (req, res) => {
  const xml = libxmljs.parseXml(fs.readFileSync('users.xml', 'utf8'));
  // ruleid: mois-1-09-xpath-injection-js
  const u = xml.get('//user[name="' + req.query.name + '"]');
  res.json({ u: u && u.text() });
});
