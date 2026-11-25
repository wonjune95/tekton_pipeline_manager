const mysql = require('mysql');

// ruleid: mois-2-13-sensitive-comment-js
// 운영 DB 비밀번호 : a1b2c3!@
const pool = mysql.createPool({ host: process.env.DB_HOST, password: process.env.DB_PASSWORD });

/*
 * 테스트 계정
// ruleid: mois-2-13-sensitive-comment-js
 * password = Spring2024!
 */
function connect() {
  // ruleid: mois-2-13-sensitive-comment-js
  // Password for administrator is "tiger"
  return pool.getConnection();
}

// ruleid: mois-2-13-sensitive-comment-js
// DB연결 root / a1q2w3r3f2!@
module.exports = { connect };
// ruleid: mois-2-13-sensitive-comment-js
const legacy = true; // 관리자 admin/Adm1n!234
