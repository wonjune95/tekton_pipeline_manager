const crypto = require('crypto');

function make(pw, salt) {
  // ok: mois-2-07-insufficient-key-length-js RSA 3072
  const rsa = crypto.generateKeyPairSync('rsa', { modulusLength: 3072 });
  // ok: mois-2-07-insufficient-key-length-js P-256
  const ec = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
  // ok: mois-2-07-insufficient-key-length-js secp384r1
  const ecdh = crypto.createECDH('secp384r1');
  // ok: mois-2-07-insufficient-key-length-js 2048비트 DH 그룹
  const dh = crypto.getDiffieHellman('modp14');
  // ok: mois-2-07-insufficient-key-length-js AES-256
  const aes = crypto.generateKeySync('aes', { length: 256 });
  // ok: mois-2-07-insufficient-key-length-js 32바이트 키
  const secretKey = crypto.randomBytes(32);
  // ok: mois-2-07-insufficient-key-length-js 8바이트 난수지만 키가 아님(요청 ID)
  const requestId = crypto.randomBytes(8).toString('hex');
  // ok: mois-2-07-insufficient-key-length-js 32바이트 유도
  const dk = crypto.pbkdf2Sync(pw, salt, 310000, 32, 'sha256');
  return [rsa, ec, ecdh, dh, aes, secretKey, requestId, dk];
}
