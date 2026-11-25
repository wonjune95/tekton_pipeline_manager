const jwt = require('jsonwebtoken');
const crypto = require('crypto');

function check(token, key) {
  // ok: mois-2-10-improper-signature-verification-js 알고리즘 고정
  return jwt.verify(token, key, { algorithms: ['RS256'] });
}

function verifyWebhook(body, sig, expected, pubKey) {
  // ok: mois-2-10-improper-signature-verification-js 결과로 거부
  if (!crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    throw new Error('bad signature');
  }
  // ok: mois-2-10-improper-signature-verification-js 결과를 변수에 받아 확인
  const ok = crypto.verify('sha256', Buffer.from(body), pubKey, Buffer.from(sig, 'base64'));
  if (!ok) throw new Error('bad signature');
  return JSON.parse(body);
}

function verifyRelease(data, sig, pubKey) {
  const v = crypto.createVerify('RSA-SHA256');
  v.update(data);
  // ok: mois-2-10-improper-signature-verification-js 결과를 반환
  return v.verify(pubKey, sig, 'base64');
}
module.exports = { check, verifyWebhook, verifyRelease };

// ok: mois-2-10-improper-signature-verification-js 사용자 정의 미들웨어 함수 (crypto 검증 아님)
function serve(file, res, next) {
  verify(file, res, next);
}
