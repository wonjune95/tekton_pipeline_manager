const crypto = require('crypto');
const CryptoJS = require('crypto-js');
const forge = require('node-forge');

function digest(data, key) {
  // ruleid: mois-2-04-weak-hash-js
  const a = crypto.createHash('md5').update(data).digest('hex');
  // ruleid: mois-2-04-weak-hash-js
  const b = crypto.createHash('SHA1').update(data).digest('hex');
  // ruleid: mois-2-04-weak-hash-js
  const c = crypto.createHmac('sha1', key).update(data).digest('hex');
  // ruleid: mois-2-04-weak-hash-js
  const d = crypto.hash('md5', data);
  // ruleid: mois-2-04-weak-hash-js
  const e = CryptoJS.MD5(data).toString();
  // ruleid: mois-2-04-weak-hash-js
  const f = CryptoJS.SHA1(data).toString();
  // ruleid: mois-2-04-weak-hash-js
  const g = CryptoJS.HmacMD5(data, key).toString();
  // ruleid: mois-2-04-weak-hash-js
  const h = CryptoJS.HmacSHA1(data, key).toString();
  // ruleid: mois-2-04-weak-hash-js
  const i = forge.md.md5.create();
  // ruleid: mois-2-04-weak-hash-js
  const j = forge.md.sha1.create();
  return [a, b, c, d, e, f, g, h, i, j];
}
