const fs = require('fs');
const mysql = require('mysql');
const db = require('./db');

function appendLine(file, line) {
  // ok: mois-5-02-resource-leak-js finally 에서 닫는다
  const fd = fs.openSync(file, 'a');
  try {
    fs.writeSync(fd, line + '\n');
  } finally {
    fs.closeSync(fd);
  }
}

function countUsers(cb) {
  let conn;
  try {
    // ok: mois-5-02-resource-leak-js finally 에서 end()
    conn = mysql.createConnection({ host: 'db' });
    conn.query('SELECT 1', cb);
  } catch (e) {
    cb(e);
  } finally {
    conn.end();
  }
}

function open(file) {
  // ok: mois-5-02-resource-leak-js 호출한 쪽이 닫는다
  const fd = fs.openSync(file, 'r');
  return fd;
}

function other() {
  // ok: mois-5-02-resource-leak-js mysql 이 아닌 객체의 createConnection
  const c = db.createConnection();
  c.ping();
}

class Store {
  init() {
    // ok: mois-5-02-resource-leak-js 필드에 담아 객체 수명 동안 쓴다
    const conn = mysql.createConnection({ host: 'db' });
    this.conn = conn;
  }
}

function reader(file) {
  // ok: mois-5-02-resource-leak-js 감싼 객체가 닫는다
  const fd = fs.openSync(file, 'r');
  return new FdReader(fd);
}
