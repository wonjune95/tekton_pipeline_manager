const mysql = require('mysql');

// ok: mois-2-13-sensitive-comment-js 값 없이 설명만
// 비밀번호는 환경변수 DB_PASSWORD 에서 읽는다
const pool = mysql.createPool({ host: process.env.DB_HOST, password: process.env.DB_PASSWORD });

/**
 * ok: mois-2-13-sensitive-comment-js 자리표시자
 * password: ${DB_PASSWORD}
 * @param password - 사용자가 입력한 비밀번호
 */
function connect(password) {
  // ok: mois-2-13-sensitive-comment-js 가린 값
  // password = ********
  // ok: mois-2-13-sensitive-comment-js 주석 처리한 코드
  // password = hash(req.body.password)
  return pool.getConnection(password);
}

// ok: mois-2-13-sensitive-comment-js 문자열 안의 // 는 주석이 아님
const url = 'http://example.com/?password=abc123!';
// ok: mois-2-13-sensitive-comment-js 경로
// see src/user/app1.js
module.exports = { connect, url };
