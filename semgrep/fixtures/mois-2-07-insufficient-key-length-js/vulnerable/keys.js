const crypto = require('crypto');
const forge = require('node-forge');

function make(pw, salt) {
  const rsa = crypto.generateKeyPairSync('rsa', {
    // ruleid: mois-2-07-insufficient-key-length-js
    modulusLength: 1024,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
  });
  // ruleid: mois-2-07-insufficient-key-length-js
  crypto.generateKeyPair('dsa', { modulusLength: 1024, divisorLength: 160 }, () => {});
  // ruleid: mois-2-07-insufficient-key-length-js
  crypto.generateKeyPair('dh', { primeLength: 1024 }, () => {});
  // ruleid: mois-2-07-insufficient-key-length-js
  const dh = crypto.createDiffieHellman(512);
  // ruleid: mois-2-07-insufficient-key-length-js
  const dh2 = crypto.getDiffieHellman('modp2');
  // ruleid: mois-2-07-insufficient-key-length-js
  const ec = crypto.generateKeyPairSync('ec', { namedCurve: 'secp192k1' });
  // ruleid: mois-2-07-insufficient-key-length-js
  const ecdh = crypto.createECDH('secp224r1');
  // ruleid: mois-2-07-insufficient-key-length-js
  const aes = crypto.generateKeySync('aes', { length: 64 });
  // ruleid: mois-2-07-insufficient-key-length-js
  const secretKey = crypto.randomBytes(8);
  // ruleid: mois-2-07-insufficient-key-length-js
  const dk = crypto.pbkdf2Sync(pw, salt, 100000, 8, 'sha256');
  // ruleid: mois-2-07-insufficient-key-length-js
  const sk = crypto.scryptSync(pw, salt, 8);
  // ruleid: mois-2-07-insufficient-key-length-js
  const kp = forge.pki.rsa.generateKeyPair(512);
  // ruleid: mois-2-07-insufficient-key-length-js
  const kp2 = forge.pki.rsa.generateKeyPair({ bits: 1024, e: 0x10001 });
  return [rsa, dh, dh2, ec, ecdh, aes, secretKey, dk, sk, kp, kp2];
}
