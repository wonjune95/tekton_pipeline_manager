const fs = require('fs');
const mysql = require('mysql');

function appendLine(file, line) {
  // ruleid: mois-5-02-resource-leak-js
  const fd = fs.openSync(file, 'a');
  fs.writeSync(fd, line + '\n');
  fs.closeSync(fd);
}

function countUsers(cb) {
  // ruleid: mois-5-02-resource-leak-js
  const conn = mysql.createConnection({ host: 'db', user: 'app' });
  conn.query('SELECT COUNT(*) AS n FROM users', (err, rows) => cb(err, rows));
}

const peek = (file) => {
  // ruleid: mois-5-02-resource-leak-js
  const fd = fs.openSync(file, 'r');
  const buf = Buffer.alloc(16);
  fs.readSync(fd, buf, 0, 16, 0);
  return buf;
};

function size(file) {
  // ruleid: mois-5-02-resource-leak-js
  const fd = fs.openSync(file, 'r');
  return fs.fstatSync(fd).size;
}
