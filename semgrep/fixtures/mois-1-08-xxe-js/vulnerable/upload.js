// 엔티티 치환을 켠 libxmljs 파싱
const libxmljs = require('libxmljs');

function importProducts(req, res) {
  // ruleid: mois-1-08-xxe-js
  const doc = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), { noent: true, noblanks: true });
  res.json(doc.root().text());
}

function loadDtd(xml) {
  const opts = { dtdload: true };
  // ruleid: mois-1-08-xxe-js
  return libxmljs.parseXml(xml, opts);
}
