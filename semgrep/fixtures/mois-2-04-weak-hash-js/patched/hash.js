const crypto = require('crypto');
const CryptoJS = require('crypto-js');

function digest(data, key) {
  // ok: mois-2-04-weak-hash-js SHA-256
  const a = crypto.createHash('sha256').update(data).digest('hex');
  // ok: mois-2-04-weak-hash-js HMAC-SHA256
  const b = crypto.createHmac('sha256', key).update(data).digest('hex');
  // ok: mois-2-04-weak-hash-js SHA-512
  const c = crypto.hash('sha512', data);
  // ok: mois-2-04-weak-hash-js CryptoJS SHA-256
  const d = CryptoJS.SHA256(data).toString();
  return [a, b, c, d];
}
