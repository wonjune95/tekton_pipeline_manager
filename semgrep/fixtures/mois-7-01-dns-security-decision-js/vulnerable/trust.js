const dns = require('dns');

function isInternal(req, cb) {
  dns.reverse(req.socket.remoteAddress, (err, hostnames) => {
    if (err) return cb(false);
    // ruleid: mois-7-01-dns-security-decision-js
    cb(hostnames.some((h) => h.endsWith('.corp.example.com')));
  });
}

function isPartner(host, cb) {
  dns.lookup(host, function (err, address) {
    // ruleid: mois-7-01-dns-security-decision-js
    if (address === '10.1.2.3') {
      return cb(true);
    }
    cb(false);
  });
}

async function trusted(ip) {
  const names = await dns.promises.reverse(ip);
  // ruleid: mois-7-01-dns-security-decision-js
  return names[0] === 'admin.example.com';
}
