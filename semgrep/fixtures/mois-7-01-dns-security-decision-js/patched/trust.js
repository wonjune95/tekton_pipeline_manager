const dns = require('dns');
const ALLOWED_IPS = ['10.1.2.3'];

function isInternal(req) {
  // ok: mois-7-01-dns-security-decision-js 접속 IP 로 판단
  return ALLOWED_IPS.includes(req.socket.remoteAddress);
}

function logName(ip) {
  dns.reverse(ip, (err, hostnames) => {
    // ok: mois-7-01-dns-security-decision-js 기록만 한다
    logger.info('peer', hostnames);
  });
}
