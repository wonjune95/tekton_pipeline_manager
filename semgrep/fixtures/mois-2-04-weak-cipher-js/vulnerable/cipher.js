const crypto = require('crypto');
const forge = require('node-forge');
const CryptoJS = require('crypto-js');

const LEGACY_ALG = 'des-ede3-cbc';

function encrypt(text, key, iv) {
  // ruleid: mois-2-04-weak-cipher-js
  const c1 = crypto.createCipher('aes-256-cbc', key);
  // ruleid: mois-2-04-weak-cipher-js
  const d1 = crypto.createDecipher('aes-256-cbc', key);
  // ruleid: mois-2-04-weak-cipher-js
  const c2 = crypto.createCipheriv('des-cbc', key, iv);
  // ruleid: mois-2-04-weak-cipher-js
  const c3 = crypto.createCipheriv(LEGACY_ALG, key, iv);
  // ruleid: mois-2-04-weak-cipher-js
  const c4 = crypto.createCipheriv('aes-128-ecb', key, null);
  // ruleid: mois-2-04-weak-cipher-js
  const c5 = crypto.createDecipheriv('bf-cbc', key, iv);
  // ruleid: mois-2-04-weak-cipher-js
  const c6 = crypto.createCipheriv('RC4', key, '');
  // ruleid: mois-2-04-weak-cipher-js
  const f1 = forge.cipher.createCipher('3DES-CBC', key);
  // ruleid: mois-2-04-weak-cipher-js
  const f2 = forge.cipher.createDecipher('AES-ECB', key);
  // ruleid: mois-2-04-weak-cipher-js
  const j1 = CryptoJS.DES.encrypt(text, key);
  // ruleid: mois-2-04-weak-cipher-js
  const j2 = CryptoJS.TripleDES.decrypt(text, key);
  // ruleid: mois-2-04-weak-cipher-js
  const j3 = CryptoJS.RC4.encrypt(text, key);
  // ruleid: mois-2-04-weak-cipher-js
  const j4 = CryptoJS.AES.encrypt(text, key, { mode: CryptoJS.mode.ECB });
  return [c1, d1, c2, c3, c4, c5, c6, f1, f2, j1, j2, j3, j4];
}
