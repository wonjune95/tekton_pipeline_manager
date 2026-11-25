const crypto = require('crypto');
const forge = require('node-forge');
const CryptoJS = require('crypto-js');

function encrypt(text, key) {
  const iv = crypto.randomBytes(12);
  // ok: mois-2-04-weak-cipher-js AES-GCM, 무작위 IV
  const c = crypto.createCipheriv('aes-256-gcm', key, iv);
  // ok: mois-2-04-weak-cipher-js AES-CBC
  const c2 = crypto.createCipheriv('aes-128-cbc', key, crypto.randomBytes(16));
  // ok: mois-2-04-weak-cipher-js 국산 알고리즘 ARIA
  const c3 = crypto.createCipheriv('aria-256-gcm', key, iv);
  // ok: mois-2-04-weak-cipher-js node-forge AES-GCM (forge 의 createCipher 는 IV 를 start() 로 받는다)
  const f = forge.cipher.createCipher('AES-GCM', key);
  f.start({ iv: forge.random.getBytesSync(12) });
  // ok: mois-2-04-weak-cipher-js CryptoJS AES 기본 모드(CBC)
  const j = CryptoJS.AES.encrypt(text, key, { mode: CryptoJS.mode.CBC });
  return [c, c2, c3, f, j];
}
