const fs = require('fs');
const https = require('https');
const tls = require('tls');

// ok: mois-2-11-improper-cert-validation-js 사설 CA 를 신뢰 저장소에 추가
const agent = new https.Agent({ ca: fs.readFileSync('/etc/ssl/private-ca.pem'), rejectUnauthorized: true });

function connect(host) {
  return tls.connect({
    host,
    port: 443,
    // ok: mois-2-11-improper-cert-validation-js 기본 검증 뒤 핀 고정 추가
    checkServerIdentity: (name, cert) => {
      const err = tls.checkServerIdentity(name, cert);
      if (err) return err;
      if (cert.fingerprint256 !== process.env.PINNED_FP) return new Error('pin mismatch');
      return undefined;
    },
  });
}
module.exports = { agent, connect };
// ok: mois-2-11-improper-cert-validation-js 검증을 켬
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '1';
