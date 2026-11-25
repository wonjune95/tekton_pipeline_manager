const jwt = require('jsonwebtoken');
const crypto = require('crypto');

function check(token, key) {
  // ruleid: mois-2-10-improper-signature-verification-js
  return jwt.verify(token, key, { algorithms: ['HS256', 'none'] });
}

function issue(payload) {
  // ruleid: mois-2-10-improper-signature-verification-js
  return jwt.sign(payload, '', { algorithm: 'none' });
}

function verifyWebhook(body, sig, expected, pubKey) {
  // ruleid: mois-2-10-improper-signature-verification-js
  crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected));
  // ruleid: mois-2-10-improper-signature-verification-js
  crypto.verify('sha256', Buffer.from(body), pubKey, Buffer.from(sig, 'base64'));
  return JSON.parse(body);
}

function verifyRelease(data, sig, pubKey) {
  const v = crypto.createVerify('RSA-SHA256');
  v.update(data);
  // ruleid: mois-2-10-improper-signature-verification-js
  v.verify(pubKey, sig, 'base64');
  return data;
}
module.exports = { check, issue, verifyWebhook, verifyRelease };
