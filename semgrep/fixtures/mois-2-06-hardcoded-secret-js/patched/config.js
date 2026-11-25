const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const mysql = require('mysql');

// ok: mois-2-06-hardcoded-secret-js 환경변수
const DB_PASSWORD = process.env.DB_PASSWORD;
// ok: mois-2-06-hardcoded-secret-js 저장소 키 이름
const ACCESS_TOKEN = 'accessToken';
// ok: mois-2-06-hardcoded-secret-js 필드 이름
const passwordField = 'password';
// ok: mois-2-06-hardcoded-secret-js 헤더 이름
const csrfToken = 'X-CSRF-TOKEN';
// ok: mois-2-06-hardcoded-secret-js 빈 값
let token = '';

const pool = mysql.createPool({
  host: 'db.internal',
  // ok: mois-2-06-hardcoded-secret-js 환경변수
  password: process.env.DB_PASSWORD,
});

const messages = {
  // ok: mois-2-06-hardcoded-secret-js 안내 문구
  password: '비밀번호를 입력하세요',
  // ok: mois-2-06-hardcoded-secret-js 자리표시자
  apiKey: '${API_KEY}',
};

function issue(user) {
  // ok: mois-2-06-hardcoded-secret-js 키는 환경변수에서
  return jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
}

function isPasswordInput(input) {
  // ok: mois-2-06-hardcoded-secret-js 입력 종류 비교
  return input.type === 'password';
}

const hmac = (data) => crypto.createHmac('sha256', process.env.HMAC_KEY).update(data).digest('hex');

// ok: mois-2-06-hardcoded-secret-js 계정 없는 접속 URL
const MONGO_URL = 'mongodb://mongo.internal:27017/app';
module.exports = { DB_PASSWORD, ACCESS_TOKEN, passwordField, csrfToken, token, pool, messages, issue, isPasswordInput, hmac, MONGO_URL };
