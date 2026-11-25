const https = require('https');
const tls = require('tls');
const axios = require('axios');
const request = require('request');
const superagent = require('superagent');
const { Pool } = require('pg');

// ruleid: mois-2-11-improper-cert-validation-js
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// ruleid: mois-2-11-improper-cert-validation-js
const agent = new https.Agent({ rejectUnauthorized: false });
const client = axios.create({ baseURL: 'https://api.example.com', httpsAgent: agent });

// ruleid: mois-2-11-improper-cert-validation-js
const pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });

function connect(host) {
  return tls.connect({
    host,
    port: 443,
    // ruleid: mois-2-11-improper-cert-validation-js
    checkServerIdentity: () => undefined,
  });
}

function connect2(host) {
  return tls.connect(443, host, {
    // ruleid: mois-2-11-improper-cert-validation-js
    checkServerIdentity: function (servername, cert) {},
  });
}

function legacy(url, cb) {
  // ruleid: mois-2-11-improper-cert-validation-js
  request({ url, strictSSL: false }, cb);
  // ruleid: mois-2-11-improper-cert-validation-js
  return superagent.get(url).disableTLSCerts();
}

function opts() {
  const o = {};
  // ruleid: mois-2-11-improper-cert-validation-js
  o.rejectUnauthorized = false;
  return o;
}
module.exports = { client, pool, connect, connect2, legacy, opts };
